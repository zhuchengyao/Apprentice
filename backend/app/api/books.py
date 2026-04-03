import os
import uuid

import aiofiles
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import get_db
from app.models.book import Book, BookStatus, Chapter, Section, KnowledgePoint
from app.schemas.book import (
    BookResponse,
    BookListResponse,
    BookDetailResponse,
    ChapterResponse,
    SectionResponse,
    KnowledgePointResponse,
)
from app.tasks.processing import process_book

router = APIRouter()


def _book_to_response(book: Book) -> BookResponse:
    return BookResponse(
        id=str(book.id),
        title=book.title,
        author=book.author,
        cover_url=book.cover_url,
        file_type=book.file_type,
        total_pages=book.total_pages,
        status=book.status.value,
        created_at=book.created_at,
        updated_at=book.updated_at,
    )


@router.post("/upload", response_model=BookResponse)
async def upload_book(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    allowed_types = ["application/pdf", "application/epub+zip", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"File type {file.content_type} not supported")

    os.makedirs(settings.upload_dir, exist_ok=True)
    file_ext = os.path.splitext(file.filename or "upload")[1]
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.upload_dir, f"{file_id}{file_ext}")

    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    book = Book(
        title=os.path.splitext(file.filename or "Untitled")[0],
        file_path=file_path,
        file_type=file_ext.lstrip("."),
        status=BookStatus.uploading,
    )
    db.add(book)
    await db.commit()
    await db.refresh(book)

    background_tasks.add_task(process_book, str(book.id))

    return _book_to_response(book)


@router.get("", response_model=BookListResponse)
async def list_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).order_by(Book.created_at.desc()))
    books = result.scalars().all()

    responses = []
    for b in books:
        resp = _book_to_response(b)
        # Count KPs for this book
        kp_count = await db.execute(
            select(func.count(KnowledgePoint.id))
            .join(Section)
            .join(Chapter)
            .where(Chapter.book_id == b.id)
        )
        resp.total_knowledge_points = kp_count.scalar() or 0
        responses.append(resp)

    return BookListResponse(books=responses)


@router.get("/{book_id}", response_model=BookDetailResponse)
async def get_book(book_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Book)
        .where(Book.id == uuid.UUID(book_id))
        .options(
            selectinload(Book.chapters)
            .selectinload(Chapter.sections)
            .selectinload(Section.knowledge_points)
        )
    )
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    total_kps = 0
    chapters_resp = []
    for chapter in book.chapters:
        sections_resp = []
        for section in chapter.sections:
            kps = [
                KnowledgePointResponse(
                    id=str(kp.id),
                    section_id=str(kp.section_id),
                    concept=kp.concept,
                    explanation=kp.explanation,
                    difficulty=kp.difficulty,
                    order_index=kp.order_index,
                    mastery_level=1.0 if kp.mastered_at else 0.0,
                )
                for kp in section.knowledge_points
            ]
            total_kps += len(kps)
            mastered_in_section = sum(1 for kp in section.knowledge_points if kp.mastered_at)
            sec_progress = mastered_in_section / len(kps) if kps else 0.0
            sections_resp.append(
                SectionResponse(
                    id=str(section.id),
                    chapter_id=str(section.chapter_id),
                    title=section.title,
                    order_index=section.order_index,
                    summary=section.summary,
                    knowledge_points=kps,
                    progress=sec_progress,
                )
            )
        ch_kp_total = sum(len(s.knowledge_points) for s in sections_resp)
        ch_kp_mastered = sum(
            sum(1 for kp in sec.knowledge_points if kp.mastery_level > 0)
            for sec in sections_resp
        )
        chapters_resp.append(
            ChapterResponse(
                id=str(chapter.id),
                book_id=str(chapter.book_id),
                title=chapter.title,
                order_index=chapter.order_index,
                summary=chapter.summary,
                sections=sections_resp,
                progress=ch_kp_mastered / ch_kp_total if ch_kp_total else 0.0,
            )
        )

    total_mastered = sum(
        1 for ch in book.chapters
        for sec in ch.sections
        for kp in sec.knowledge_points
        if kp.mastered_at
    )

    return BookDetailResponse(
        id=str(book.id),
        title=book.title,
        author=book.author,
        cover_url=book.cover_url,
        file_type=book.file_type,
        total_pages=book.total_pages,
        status=book.status.value,
        total_knowledge_points=total_kps,
        mastered_knowledge_points=total_mastered,
        progress=total_mastered / total_kps if total_kps else 0.0,
        created_at=book.created_at,
        updated_at=book.updated_at,
        chapters=chapters_resp,
    )


@router.get("/{book_id}/status")
async def get_book_status(book_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Book.status, Book.error_message).where(Book.id == uuid.UUID(book_id))
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": row[0].value, "error": row[1]}


@router.post("/{book_id}/reprocess-images")
async def reprocess_images(book_id: str, db: AsyncSession = Depends(get_db)):
    """Re-extract images from a book's PDF and rebuild section content with image refs.

    Deletes existing KPs so they are re-extracted (with image awareness) on next study.
    """
    import asyncio
    from app.services.parser.pdf_parser import parse_pdf

    result = await db.execute(
        select(Book)
        .where(Book.id == uuid.UUID(book_id))
        .options(
            selectinload(Book.chapters)
            .selectinload(Chapter.sections)
            .selectinload(Section.knowledge_points)
        )
    )
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.file_type != "pdf":
        raise HTTPException(status_code=400, detail="Only PDF books can be reprocessed")
    if not os.path.exists(book.file_path):
        raise HTTPException(status_code=400, detail="PDF file not found on disk")

    # Re-parse with image extraction (run in thread to avoid blocking async loop)
    loop = asyncio.get_running_loop()
    parsed = await loop.run_in_executor(
        None, lambda: parse_pdf(book.file_path, book_id=str(book.id))
    )

    # Build page → image URL mapping
    from app.tasks.processing import _page_matches_section
    page_images: dict[int, list[str]] = {}
    page_texts: dict[int, str] = {}
    for page in parsed.pages:
        text = page.text.strip()
        if text:
            page_texts[page.page_number] = text
        for img in page.images:
            page_images.setdefault(page.page_number, []).append(img.image_url)

    total_images = len(parsed.images)
    kps_deleted = 0

    for chapter in book.chapters:
        for section in chapter.sections:
            raw = section.content_raw or ""
            # Strip any previous injected images
            marker = "\n\n---\n## Book Figures\n"
            if marker in raw:
                raw = raw[:raw.index(marker)]

            # Match images to this section using page text overlap
            matched = []
            for page_num in sorted(page_images.keys()):
                if page_num not in page_texts:
                    continue
                if _page_matches_section(page_texts[page_num], raw):
                    for url in page_images[page_num]:
                        matched.append(f"![Figure from page {page_num}]({url})")

            if matched and "/api/images/" not in raw:
                section.content_raw = raw + "\n\n" + "\n\n".join(matched)
            else:
                section.content_raw = raw

            for kp in section.knowledge_points:
                await db.delete(kp)
                kps_deleted += 1

    await db.commit()

    return {
        "status": "ok",
        "images_extracted": total_images,
        "kps_deleted": kps_deleted,
        "message": f"Extracted {total_images} images. Deleted {kps_deleted} KPs — they will be re-generated with figure awareness on next study.",
    }


@router.delete("/{book_id}")
async def delete_book(book_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == uuid.UUID(book_id)))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if os.path.exists(book.file_path):
        os.remove(book.file_path)
    await db.delete(book)
    await db.commit()
    return {"status": "deleted"}
