import asyncio
import json
import logging
import os

from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.pool import NullPool

from app.config import settings
from app.constants import (
    BATCH_SIZE,
    ILLUSTRATION_CONCURRENCY,
    ILLUSTRATION_MIN_DIFFICULTY,
    ILLUSTRATION_QUALITY,
)
from app.models.book import Book, BookPage, BookStatus, Chapter, Section, KnowledgePoint
from app.services.ai_context import ai_user_context
from app.services.extractor.manim_v2 import (
    ManimInput,
    ManimOutcome,
    generate_manim_batch,
    log_manim_outcome,
)
from app.services.extractor.knowledge import extract_knowledge_points
from app.services.parser.pdf_parser import parse_pdf_metadata
from app.services.parser.vision_converter import convert_page_batch

logger = logging.getLogger(__name__)


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

    # Serialize concurrent chapter workers for the same book. Overlapping
    # chapter page-ranges (common when the TOC has level-1 + level-2
    # entries that share pages) would otherwise race on the per-row
    # INSERT ... ON CONFLICT lock and occasionally deadlock. The xact
    # lock auto-releases on commit/rollback.
    await db.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"),
        {"key": f"book_pages:{book_id}"},
    )

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

    try:
        await _extract_chapter_knowledge(db, chapter, book)
    except Exception as e:
        logger.error(
            "KP extraction failed for chapter '%s' (%s): %s — continuing without KPs",
            chapter.title, chapter.id, e,
        )

    chapter.processed = True
    await db.flush()

    logger.info("Chapter '%s' complete (%d pages)", chapter.title, total)


async def _extract_chapter_knowledge(
    db: AsyncSession,
    chapter: Chapter,
    book: Book,
):
    """Pull all converted pages for a chapter, extract KPs, persist Section + KPs.

    Creates one synthetic Section per chapter to preserve the current
    Chapter → Section → KP model. Idempotent: skips if KPs already exist
    for this chapter.
    """
    existing = await db.execute(
        select(Section.id).where(Section.chapter_id == chapter.id).limit(1)
    )
    if existing.scalar_one_or_none() is not None:
        logger.info("Chapter '%s' already has a Section — skipping KP extraction", chapter.title)
        return

    pages_result = await db.execute(
        select(BookPage)
        .where(
            BookPage.book_id == book.id,
            BookPage.page_number >= chapter.start_page,
            BookPage.page_number <= chapter.end_page,
        )
        .order_by(BookPage.page_number)
    )
    pages = pages_result.scalars().all()
    if not pages:
        logger.warning("No pages found for chapter '%s' — skipping KP extraction", chapter.title)
        return

    content = "\n\n".join(p.html_content for p in pages if p.html_content)
    if not content.strip():
        logger.warning("Empty content for chapter '%s' — skipping KP extraction", chapter.title)
        return

    result = await extract_knowledge_points(chapter.title, content)
    kps = result.get("knowledge_points") or []
    if not kps:
        logger.warning("No KPs returned for chapter '%s'", chapter.title)
        return

    section = Section(
        chapter_id=chapter.id,
        title=chapter.title,
        order_index=0,
        content_markdown=content,
        summary=result.get("section_summary"),
    )
    db.add(section)
    await db.flush()

    # Decide which KPs get an animation before inserting — skip trivial
    # facts (difficulty == 1). Heavy concepts benefit most from a visual,
    # and Manim rendering is expensive (LLM + subprocess + FFmpeg).
    illustration_targets: list[tuple[int, ManimInput]] = [
        (
            idx,
            ManimInput(
                concept=(kp.get("concept") or "")[:300],
                explanation=(kp.get("explanation") or "")[:2000],
                chapter_title=chapter.title,
                section_title=section.title,
                kp_index=idx,
            ),
        )
        for idx, kp in enumerate(kps)
        if int(kp.get("difficulty") or 1) >= ILLUSTRATION_MIN_DIFFICULTY
        and (kp.get("concept") or "").strip()
    ]
    outcomes_by_idx: dict[int, ManimOutcome] = {}
    video_filenames: dict[int, str] = {}
    if illustration_targets:
        outcomes = await generate_manim_batch(
            [inp for _, inp in illustration_targets],
            concurrency=ILLUSTRATION_CONCURRENCY,
            quality=ILLUSTRATION_QUALITY,
        )
        for (idx, _), outcome in zip(illustration_targets, outcomes):
            outcomes_by_idx[idx] = outcome
            if outcome.output_path is not None:
                video_filenames[idx] = outcome.output_path.name

    kp_rows: list[tuple[int, KnowledgePoint]] = []
    for idx, kp in enumerate(kps):
        image_refs = kp.get("image_refs") or []
        image_urls = json.dumps(image_refs) if image_refs else None
        row = KnowledgePoint(
            section_id=section.id,
            concept=(kp.get("concept") or "")[:500],
            explanation=kp.get("explanation") or "",
            difficulty=int(kp.get("difficulty") or 1),
            order_index=int(kp.get("order_index", idx)),
            image_urls=image_urls,
            source_anchor=kp.get("source_anchor") or None,
            illustration_video=video_filenames.get(idx),
        )
        db.add(row)
        kp_rows.append((idx, row))
    await db.flush()

    # After flush, KP rows have real ids — emit one structured log record per
    # animation attempt (success or failure) so acceptance rate and failure
    # modes are visible in logs.
    for idx, row in kp_rows:
        outcome = outcomes_by_idx.get(idx)
        if outcome is None:
            continue
        log_manim_outcome(
            outcome,
            book_id=str(book.id),
            chapter_id=str(chapter.id),
            kp_id=str(row.id),
            concept=row.concept,
        )

    logger.info(
        "Chapter '%s': extracted %d KPs (%d animated)",
        chapter.title, len(kps), len(video_filenames),
    )


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

            user_id = str(chapter.book.user_id) if chapter.book.user_id else None
            try:
                with ai_user_context(user_id):
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
