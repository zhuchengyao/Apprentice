import asyncio
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sse_starlette.sse import EventSourceResponse

from app.database import get_db
from app.dependencies import get_current_user
from app.models.book import Book, BookPage, Chapter
from app.models.user import User
from app.schemas.book import BookPageResponse, BookPagesResponse, ChapterResponse

router = APIRouter()


async def _get_user_book(
    book_id: str, current_user: User, db: AsyncSession
) -> Book:
    """Load a book owned by current_user, or raise 404."""
    result = await db.execute(
        select(Book).where(
            Book.id == uuid.UUID(book_id),
            Book.user_id == current_user.id,
        )
    )
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


async def _get_user_chapter(
    book_id: str,
    chapter_id: str,
    current_user: User,
    db: AsyncSession,
    *,
    load_book: bool = False,
) -> Chapter:
    """Load a chapter whose parent book is owned by current_user, or raise 404."""
    query = (
        select(Chapter)
        .join(Book, Book.id == Chapter.book_id)
        .where(
            Chapter.id == uuid.UUID(chapter_id),
            Chapter.book_id == uuid.UUID(book_id),
            Book.user_id == current_user.id,
        )
    )
    if load_book:
        query = query.options(selectinload(Chapter.book))
    result = await db.execute(query)
    chapter = result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@router.get("/{book_id}/pages/{page_number}", response_model=BookPageResponse)
async def get_page(
    book_id: str,
    page_number: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _get_user_book(book_id, current_user, db)
    result = await db.execute(
        select(BookPage)
        .where(BookPage.book_id == uuid.UUID(book_id), BookPage.page_number == page_number)
    )
    page = result.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return BookPageResponse(page_number=page.page_number, html_content=page.html_content)


@router.get("/{book_id}/pages", response_model=BookPagesResponse)
async def get_pages(
    book_id: str,
    start: int = Query(1, ge=1),
    end: int = Query(None, ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = await _get_user_book(book_id, current_user, db)

    query = (
        select(BookPage)
        .where(BookPage.book_id == uuid.UUID(book_id), BookPage.page_number >= start)
    )
    if end is not None:
        query = query.where(BookPage.page_number <= end)

    query = query.order_by(BookPage.page_number)
    result = await db.execute(query)
    pages = result.scalars().all()

    return BookPagesResponse(
        book_id=book_id,
        total_pages=book.total_pages,
        pages=[BookPageResponse(page_number=p.page_number, html_content=p.html_content) for p in pages],
    )


@router.get("/{book_id}/chapters/{chapter_id}/pages", response_model=BookPagesResponse)
async def get_chapter_pages(
    book_id: str,
    chapter_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all HTML pages belonging to a chapter."""
    chapter = await _get_user_chapter(
        book_id, chapter_id, current_user, db, load_book=True
    )

    pages_result = await db.execute(
        select(BookPage)
        .where(
            BookPage.book_id == uuid.UUID(book_id),
            BookPage.page_number >= chapter.start_page,
            BookPage.page_number <= chapter.end_page,
        )
        .order_by(BookPage.page_number)
    )
    pages = pages_result.scalars().all()

    return BookPagesResponse(
        book_id=book_id,
        total_pages=chapter.book.total_pages,
        pages=[BookPageResponse(page_number=p.page_number, html_content=p.html_content) for p in pages],
    )


@router.get("/{book_id}/chapters/{chapter_id}/progress")
async def get_chapter_progress(
    book_id: str,
    chapter_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return processing progress for a chapter (pages done vs total)."""
    chapter = await _get_user_chapter(book_id, chapter_id, current_user, db)

    pages_total = max(chapter.end_page - chapter.start_page + 1, 0)

    count_result = await db.execute(
        select(func.count(BookPage.id)).where(
            BookPage.book_id == uuid.UUID(book_id),
            BookPage.page_number >= chapter.start_page,
            BookPage.page_number <= chapter.end_page,
        )
    )
    pages_done = count_result.scalar() or 0

    return {
        "chapter_id": chapter_id,
        "processed": chapter.processed,
        "pages_done": pages_done,
        "pages_total": pages_total,
    }


@router.post("/{book_id}/chapters/{chapter_id}/process")
async def process_chapter_endpoint(
    book_id: str,
    chapter_id: str,
    force: bool = Query(False, description="Force reprocess: delete existing pages and redo"),
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Start processing a chapter in the background. Returns immediately.

    Use ?force=true to delete existing pages and reprocess from scratch.
    """
    chapter = await _get_user_chapter(book_id, chapter_id, current_user, db)

    pages_total = max(chapter.end_page - chapter.start_page + 1, 0)

    if force:
        # Delete existing pages for this chapter and reset processed flag
        from sqlalchemy import delete
        await db.execute(
            delete(BookPage).where(
                BookPage.book_id == uuid.UUID(book_id),
                BookPage.page_number >= chapter.start_page,
                BookPage.page_number <= chapter.end_page,
            )
        )
        chapter.processed = False
        await db.commit()
    elif chapter.processed:
        return {
            "status": "already_processed",
            "chapter_id": chapter_id,
            "pages_done": pages_total,
            "pages_total": pages_total,
        }
    else:
        # Guard: if pages already exist for this chapter, processing is likely underway
        count_result = await db.execute(
            select(func.count(BookPage.id)).where(
                BookPage.book_id == uuid.UUID(book_id),
                BookPage.page_number >= chapter.start_page,
                BookPage.page_number <= chapter.end_page,
            )
        )
        existing = count_result.scalar() or 0
        if existing > 0:
            return {
                "status": "processing",
                "chapter_id": chapter_id,
                "pages_done": existing,
                "pages_total": pages_total,
            }

    from app.tasks.processing import process_chapter_sync
    background_tasks.add_task(process_chapter_sync, str(chapter.id))

    return {
        "status": "processing",
        "chapter_id": chapter_id,
        "pages_done": 0,
        "pages_total": pages_total,
    }


@router.post("/{book_id}/pages/{page_number}/reprocess")
async def reprocess_page(
    book_id: str,
    page_number: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Re-convert a single page via vision model (costs one API call)."""
    import os
    import fitz
    from sqlalchemy.dialects.postgresql import insert as pg_insert
    from app.config import settings
    from app.services.parser.vision_converter import convert_page_batch

    book = await _get_user_book(book_id, current_user, db)

    if page_number < 1 or page_number > book.total_pages:
        raise HTTPException(status_code=400, detail=f"Page must be 1–{book.total_pages}")

    doc = fitz.open(book.file_path)
    image_dir = os.path.join(settings.upload_dir, "images", str(book.id))
    os.makedirs(image_dir, exist_ok=True)

    results = await convert_page_batch(doc, str(book.id), [page_number], image_dir)
    doc.close()

    if not results:
        raise HTTPException(status_code=500, detail="Vision conversion returned no result")

    hp = results[0]
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

    return {
        "status": "ok",
        "page_number": hp.page_number,
        "html_length": len(hp.html),
    }


@router.get("/{book_id}/pages/{page_number}/figures")
async def list_figures(
    book_id: str,
    page_number: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all figure images on a page with their filenames and URLs."""
    import re

    await _get_user_book(book_id, current_user, db)
    result = await db.execute(
        select(BookPage).where(
            BookPage.book_id == uuid.UUID(book_id),
            BookPage.page_number == page_number,
        )
    )
    page = result.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    figures = []
    for m in re.finditer(
        r'<figure[^>]*>.*?<img\s+src="([^"]+)"[^>]*alt="([^"]*)".*?</figure>',
        page.html_content,
        re.DOTALL,
    ):
        src = m.group(1).split("?")[0]  # strip cache buster
        filename = src.rsplit("/", 1)[-1]
        figures.append({
            "filename": filename,
            "src": src,
            "alt": m.group(2),
        })

    return {
        "page_number": page_number,
        "figures": figures,
    }


@router.post("/{book_id}/pages/{page_number}/fix-figure")
async def fix_figure(
    book_id: str,
    page_number: int,
    filename: str = Query(..., description="Image filename, e.g. p45_fig_abc12345.png"),
    top: float | None = Query(None, ge=0, le=100),
    left: float | None = Query(None, ge=0, le=100),
    bottom: float | None = Query(None, ge=0, le=100),
    right: float | None = Query(None, ge=0, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fix a single figure's screenshot.

    - With coordinates: pure local re-crop, zero API cost.
    - Without coordinates: GPT re-locates the figure using the alt text (~64 output tokens).

    Usage:
        # Auto re-locate (GPT finds the correct position):
        POST .../fix-figure?filename=p45_fig_abc12345.png

        # Manual coordinates:
        POST .../fix-figure?filename=p45_fig_abc12345.png&top=10&left=5&bottom=60&right=95
    """
    import os
    import re
    import time
    import fitz
    from app.config import settings
    from app.services.parser.vision_converter import _render_figure_region

    book = await _get_user_book(book_id, current_user, db)

    if page_number < 1 or page_number > book.total_pages:
        raise HTTPException(status_code=400, detail=f"Page must be 1–{book.total_pages}")

    from pathlib import Path
    image_dir = Path(settings.upload_dir).resolve() / "images" / book_id
    filepath = (image_dir / filename).resolve()
    if not filepath.is_relative_to(image_dir):
        raise HTTPException(status_code=400, detail="Invalid filename")
    if not filepath.is_file():
        raise HTTPException(status_code=404, detail=f"Image file '{filename}' not found")
    filepath = str(filepath)

    has_manual_coords = all(v is not None for v in (top, left, bottom, right))

    doc = fitz.open(book.file_path)

    if not has_manual_coords:
        # Get the figure's alt text from stored HTML to use as description
        page_result = await db.execute(
            select(BookPage).where(
                BookPage.book_id == uuid.UUID(book_id),
                BookPage.page_number == page_number,
            )
        )
        book_page = page_result.scalar_one_or_none()
        description = f"Figure on page {page_number}"
        if book_page:
            alt_match = re.search(
                re.escape(filename) + r'[^>]*alt="([^"]*)"',
                book_page.html_content,
            )
            if alt_match:
                description = alt_match.group(1)

        from app.services.parser.vision_converter import relocate_figure
        top, left, bottom, right = await relocate_figure(
            doc, page_number, description,
        )

    png_bytes = _render_figure_region(doc[page_number - 1], top, left, bottom, right)
    doc.close()

    with open(filepath, "wb") as f:
        f.write(png_bytes)

    # Bust browser cache
    page_result = await db.execute(
        select(BookPage).where(
            BookPage.book_id == uuid.UUID(book_id),
            BookPage.page_number == page_number,
        )
    )
    book_page = page_result.scalar_one_or_none()
    if book_page:
        cache_buster = f"?v={int(time.time())}"
        old_src = f"/api/images/{book_id}/{filename}"
        book_page.html_content = re.sub(
            re.escape(old_src) + r"(\?v=\d+)?",
            old_src + cache_buster,
            book_page.html_content,
        )
        await db.commit()

    return {
        "status": "ok",
        "page_number": page_number,
        "filename": filename,
        "region": {"top": top, "left": left, "bottom": bottom, "right": right},
        "size_bytes": len(png_bytes),
    }


@router.get("/{book_id}/chapters/{chapter_id}/progress/stream")
async def stream_chapter_progress(
    book_id: str,
    chapter_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """SSE endpoint that streams chapter processing progress until complete."""
    chapter = await _get_user_chapter(book_id, chapter_id, current_user, db)

    pages_total = max(chapter.end_page - chapter.start_page + 1, 0)
    book_uuid = uuid.UUID(book_id)
    chapter_uuid = uuid.UUID(chapter_id)

    async def event_generator():
        import json
        from app.database import async_session

        last_done = -1
        while True:
            # Use a short-lived session per iteration to avoid holding a connection
            async with async_session() as session:
                count_result = await session.execute(
                    select(func.count(BookPage.id)).where(
                        BookPage.book_id == book_uuid,
                        BookPage.page_number >= chapter.start_page,
                        BookPage.page_number <= chapter.end_page,
                    )
                )
                pages_done = count_result.scalar() or 0

                ch_result = await session.execute(
                    select(Chapter.processed).where(Chapter.id == chapter_uuid)
                )
                processed = ch_result.scalar()

            if pages_done != last_done or processed:
                last_done = pages_done
                data = json.dumps({
                    "chapter_id": chapter_id,
                    "pages_done": pages_done,
                    "pages_total": pages_total,
                    "processed": bool(processed),
                })
                yield {"event": "progress", "data": data}

            if processed:
                yield {"event": "done", "data": json.dumps({"chapter_id": chapter_id})}
                return

            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())
