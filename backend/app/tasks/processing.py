import asyncio
import logging
import os

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.pool import NullPool

from app.config import settings
from app.models.book import Book, BookPage, BookStatus, Chapter
from app.services.parser.pdf_parser import parse_pdf_metadata
from app.services.parser.vision_converter import convert_page_batch

logger = logging.getLogger(__name__)

BATCH_SIZE = 3



# ---------------------------------------------------------------------------
# Helpers (used by the reprocess-images endpoint in books.py)
# ---------------------------------------------------------------------------

def _extract_phrases(text: str, phrase_len: int = 30, count: int = 8) -> list[str]:
    """Extract several short phrases from different positions in the text for fuzzy matching."""
    import re
    cleaned = re.sub(r'\s+', ' ', text.strip())
    if len(cleaned) < phrase_len:
        return [cleaned] if len(cleaned) > 15 else []

    phrases = []
    step = max(1, (len(cleaned) - phrase_len) // count)
    for i in range(0, len(cleaned) - phrase_len, step):
        phrase = cleaned[i:i + phrase_len].strip()
        if len(phrase) >= 15:
            phrases.append(phrase)
        if len(phrases) >= count:
            break
    return phrases


def _page_matches_section(page_text: str, section_content: str) -> bool:
    """Check if a page's text has enough overlap with a section's content."""
    import re
    phrases = _extract_phrases(page_text)
    if not phrases:
        return False
    for phrase in phrases:
        if phrase in section_content:
            return True
    page_words = set(w.lower() for w in re.findall(r'[a-zA-Z]{5,}', page_text))
    section_words = set(w.lower() for w in re.findall(r'[a-zA-Z]{5,}', section_content))
    if not page_words:
        return False
    overlap = len(page_words & section_words) / len(page_words)
    return overlap > 0.4


# ---------------------------------------------------------------------------
# TOC → chapter list (now uses level 1 + level 2 for finer granularity)
# ---------------------------------------------------------------------------

def _chapters_from_toc(
    toc: list[tuple[int, str, int]], total_pages: int,
) -> list[dict]:
    """Build chapter list from PDF table of contents.

    Uses TOC entries up to level 2 for finer-grained processing units.
    Entries that would span 0 pages (e.g. a level-1 heading on the same page
    as its first level-2 child) are automatically filtered out.
    """
    entries = sorted(
        [(title.strip(), page) for level, title, page in toc if level <= 2 and title.strip()],
        key=lambda e: (e[1], e[0]),
    )

    chapters: list[dict] = []
    for i, (title, page) in enumerate(entries):
        next_page = entries[i + 1][1] if i + 1 < len(entries) else total_pages + 1
        end_page = next_page - 1
        if end_page >= page:
            chapters.append({
                "title": title,
                "order_index": len(chapters),
                "start_page": page,
                "end_page": min(end_page, total_pages),
            })

    if not chapters:
        chapters.append({
            "title": "Content",
            "order_index": 0,
            "start_page": 1,
            "end_page": total_pages,
        })

    return chapters


# ---------------------------------------------------------------------------
# Chapter processing (incremental batch saving)
# ---------------------------------------------------------------------------

async def process_chapter(
    db: AsyncSession,
    chapter: Chapter,
    book: Book | None = None,
):
    """Process a chapter via GPT-5.4 vision, saving pages in small batches.

    After each batch of BATCH_SIZE pages is converted, the results are flushed
    to the database so that progress is visible to polling clients.
    """
    if book is None:
        book = chapter.book
    book_id = str(book.id)

    import fitz
    doc = fitz.open(book.file_path)
    total_doc_pages = len(doc)

    start = chapter.start_page
    end = min(chapter.end_page, total_doc_pages)
    all_pages = list(range(start, end + 1))
    total = len(all_pages)

    logger.info(
        "Processing chapter '%s' (pages %d–%d, %d pages) for book '%s'",
        chapter.title, start, end, total, book.title,
    )

    image_dir = os.path.join(settings.upload_dir, "images", book_id)
    os.makedirs(image_dir, exist_ok=True)

    for batch_start in range(0, total, BATCH_SIZE):
        batch = all_pages[batch_start : batch_start + BATCH_SIZE]
        results = await convert_page_batch(doc, book_id, batch, image_dir)

        for hp in results:
            stmt = pg_insert(BookPage).values(
                book_id=book.id,
                page_number=hp.page_number,
                html_content=hp.html,
            ).on_conflict_do_update(
                constraint="uq_book_pages_book_page",
                set_={"html_content": hp.html},
            )
            await db.execute(stmt)
        await db.flush()

        done = min(batch_start + BATCH_SIZE, total)
        logger.info("Chapter '%s': %d/%d pages done", chapter.title, done, total)

    doc.close()
    chapter.processed = True
    await db.flush()

    logger.info("Chapter '%s' complete (%d pages)", chapter.title, total)


# ---------------------------------------------------------------------------
# Standalone chapter processing (for BackgroundTasks — own DB session)
# ---------------------------------------------------------------------------

async def _process_chapter_standalone(chapter_id: str):
    """Process a chapter with its own DB session and engine.

    Creates a disposable engine per invocation so that all connections
    are cleanly closed before the event loop shuts down — avoids the
    'Event loop is closed' noise from asyncpg.
    """
    engine = create_async_engine(settings.database_url, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    try:
        async with session_factory() as db:
            result = await db.execute(
                select(Chapter)
                .where(Chapter.id == chapter_id)
                .options(selectinload(Chapter.book))
            )
            chapter = result.scalar_one_or_none()
            if not chapter or chapter.processed:
                return

            try:
                await process_chapter(db, chapter)
                await db.commit()
            except Exception as e:
                logger.error("Chapter processing failed for %s: %s", chapter_id, e)
                await db.rollback()
    finally:
        await engine.dispose()


def process_chapter_sync(chapter_id: str):
    """Sync wrapper for FastAPI BackgroundTasks."""
    asyncio.run(_process_chapter_standalone(chapter_id))


# ---------------------------------------------------------------------------
# Initial book processing (upload → metadata + chapter creation)
# ---------------------------------------------------------------------------

async def _process_book(book_id: str):
    """Parse metadata + TOC → create all chapters → mark ready.

    Page content is processed lazily when the user opens a chapter.
    """
    engine = create_async_engine(settings.database_url, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    try:
        async with session_factory() as db:
            result = await db.execute(select(Book).where(Book.id == book_id))
            book = result.scalar_one_or_none()
            if not book:
                return

            try:
                book.status = BookStatus.parsing
                await db.commit()

                if book.file_type != "pdf":
                    book.status = BookStatus.error
                    book.error_message = f"Unsupported file type: {book.file_type}"
                    await db.commit()
                    return

                meta = parse_pdf_metadata(book.file_path)
                book.title = meta.title or book.title
                book.author = meta.author or book.author
                book.total_pages = meta.total_pages
                await db.commit()

                chapter_infos = _chapters_from_toc(meta.toc, meta.total_pages)
                logger.info(
                    "Book '%s': %d pages, %d sections from TOC",
                    book.title, meta.total_pages, len(chapter_infos),
                )

                for ch_info in chapter_infos:
                    db.add(Chapter(
                        book_id=book.id,
                        title=ch_info["title"],
                        order_index=ch_info["order_index"],
                        start_page=ch_info["start_page"],
                        end_page=ch_info["end_page"],
                        processed=False,
                    ))
                await db.flush()

                book.status = BookStatus.ready
                await db.commit()
                logger.info(
                    "Book '%s' ready (%d sections, pages processed on demand)",
                    book.title, len(chapter_infos),
                )

            except Exception as e:
                logger.error("Book processing failed for %s: %s", book_id, e)
                book.status = BookStatus.error
                book.error_message = str(e)
                await db.commit()
    finally:
        await engine.dispose()


def process_book(book_id: str):
    """Sync wrapper for FastAPI BackgroundTasks."""
    asyncio.run(_process_book(book_id))
