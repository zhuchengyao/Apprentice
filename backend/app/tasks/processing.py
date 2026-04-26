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
    ILLUSTRATION_QUALITY,
)
from app.models.book import Book, BookPage, BookStatus, Chapter, Section, KnowledgePoint
from app.services.ai_context import ai_user_context
from app.services.extractor.manim_v2.jobs import (
    enqueue_animation_jobs_for_kps,
    process_queued_animation_jobs_for_chapter,
)
from app.services.extractor.knowledge import extract_knowledge_points
from app.services.parser.pdf_parser import parse_pdf_metadata
from app.services.parser.vision_converter import convert_page_batch
from app.services.teaching.study_planner import (
    plan_and_persist_scopes_for_chapter,
    prewarm_scope_explanations,
)

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

    Each batch commits its own transaction so the SSE progress poller
    (which runs in a separate session under READ COMMITTED isolation) can
    actually see rows as they arrive. Holding one long transaction across
    the entire chapter — which is what `flush()`-only did — made progress
    invisible until the very end, producing a 0 → 100% jump.
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
        # Vision HTTP call is expensive; keep it OUTSIDE any DB transaction
        # so we don't hold connections/locks across network I/O.
        results = await convert_page_batch(doc, book_id, batch, image_dir)

        # Serialize concurrent chapter workers for the same book only
        # during the write window. Overlapping chapter page-ranges (common
        # with TOC level-1 + level-2) would otherwise race on the per-row
        # INSERT … ON CONFLICT lock and occasionally deadlock. The xact
        # lock auto-releases on commit.
        await db.execute(
            text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"),
            {"key": f"book_pages:{book_id}"},
        )
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
        await db.commit()

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
        )
        db.add(row)
        kp_rows.append((idx, row))
    await db.flush()

    animation_jobs = await enqueue_animation_jobs_for_kps(
        db,
        book=book,
        chapter=chapter,
        kps=[row for _, row in kp_rows],
    )

    logger.info(
        "Chapter '%s': extracted %d KPs (%d animation jobs queued)",
        chapter.title, len(kps), len(animation_jobs),
    )

    # Parse-stage scope plan. Runs once per chapter and is shared across
    # every learner's session; session creation hydrates its scope_plan
    # JSONB from these rows instead of re-calling the LLM per session.
    try:
        persisted_kps = [row for _, row in kp_rows]
        await plan_and_persist_scopes_for_chapter(
            db,
            chapter,
            book_title=book.title or "",
            chapter_content=content,
            kps=persisted_kps,
            language=settings.prewarm_language,
        )
        if settings.prewarm_scope_explanations:
            await prewarm_scope_explanations(
                db,
                chapter,
                book_title=book.title or "",
                chapter_content=content,
                kps=persisted_kps,
                language=settings.prewarm_language,
            )
    except Exception as e:
        logger.error(
            "scope prep failed for chapter '%s' (%s): %s — "
            "session-time fallback will plan on demand",
            chapter.title, chapter.id, e,
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
                try:
                    count = await process_queued_animation_jobs_for_chapter(
                        chapter.id,
                        user_id=user_id,
                        concurrency=ILLUSTRATION_CONCURRENCY,
                        quality=ILLUSTRATION_QUALITY,
                    )
                    if count:
                        logger.info(
                            "Chapter '%s': processed %d queued animation jobs",
                            chapter.title, count,
                        )
                except Exception as e:
                    logger.exception(
                        "Animation jobs failed for chapter %s after parsing completed: %s",
                        chapter_id, e,
                    )
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
