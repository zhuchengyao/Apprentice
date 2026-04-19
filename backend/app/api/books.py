import os
import uuid

import aiofiles
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.book import Book, BookStatus, Chapter, Section, KnowledgePoint
from app.models.user import User
from app.schemas.book import (
    BookResponse,
    BookListResponse,
    BookDetailResponse,
    ChapterResponse,
    SectionResponse,
    KnowledgePointResponse,
)
from app.services.billing import check_credits_or_raise
from app.services.book_reprocess import (
    reprocess_book_images,
    validate_reprocess_preconditions,
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


MAX_UPLOAD_SIZE = 500 * 1024 * 1024  # 500 MB


@router.post("/upload", response_model=BookResponse)
async def upload_book(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Currently only PDFs actually make it through _process_book; surface that
    # to the client up front instead of accepting upload → failing in the task.
    allowed_types = ["application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not supported (only PDF)",
        )

    # Pre-check credits BEFORE touching disk or inserting a DB row. If the user
    # has no balance, we don't want to leak a file or an orphan Book record.
    await check_credits_or_raise(
        db, current_user.id, model="gpt-5.4", max_tokens=4096
    )

    os.makedirs(settings.upload_dir, exist_ok=True)
    file_ext = os.path.splitext(file.filename or "upload")[1]
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.upload_dir, f"{file_id}{file_ext}")

    total_size = 0
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # 1 MB chunks
                total_size += len(chunk)
                if total_size > MAX_UPLOAD_SIZE:
                    raise HTTPException(
                        status_code=413, detail="File too large (max 500 MB)"
                    )
                await f.write(chunk)
    except BaseException:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise

    book = Book(
        user_id=current_user.id,
        title=os.path.splitext(file.filename or "Untitled")[0],
        file_path=file_path,
        file_type=file_ext.lstrip("."),
        status=BookStatus.uploading,
    )
    db.add(book)
    try:
        await db.commit()
    except BaseException:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
    await db.refresh(book)

    background_tasks.add_task(process_book, str(book.id))

    return _book_to_response(book)


@router.get("", response_model=BookListResponse)
async def list_books(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Book)
        .where(Book.user_id == current_user.id)
        .order_by(Book.created_at.desc())
    )
    books = result.scalars().all()

    # Batch-fetch KP counts for all books in one query
    book_ids = [b.id for b in books]
    kp_counts: dict = {}
    if book_ids:
        kp_result = await db.execute(
            select(Chapter.book_id, func.count(KnowledgePoint.id))
            .join(Section, Section.chapter_id == Chapter.id)
            .join(KnowledgePoint, KnowledgePoint.section_id == Section.id)
            .where(Chapter.book_id.in_(book_ids))
            .group_by(Chapter.book_id)
        )
        kp_counts = dict(kp_result.all())

    responses = []
    for b in books:
        resp = _book_to_response(b)
        resp.total_knowledge_points = kp_counts.get(b.id, 0)
        responses.append(resp)

    return BookListResponse(books=responses)


@router.get("/{book_id}", response_model=BookDetailResponse)
async def get_book(
    book_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Book)
        .where(Book.id == uuid.UUID(book_id), Book.user_id == current_user.id)
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
                start_page=chapter.start_page,
                end_page=chapter.end_page,
                processed=chapter.processed,
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
async def get_book_status(
    book_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Book.status, Book.error_message)
        .where(Book.id == uuid.UUID(book_id), Book.user_id == current_user.id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": row[0].value, "error": row[1]}


@router.post("/{book_id}/reprocess-images")
async def reprocess_images(
    book_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Re-extract images from a book's PDF and rebuild section content with image refs."""
    result = await db.execute(
        select(Book)
        .where(Book.id == uuid.UUID(book_id), Book.user_id == current_user.id)
        .options(
            selectinload(Book.chapters)
            .selectinload(Chapter.sections)
            .selectinload(Section.knowledge_points)
        )
    )
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    precondition_error = validate_reprocess_preconditions(book)
    if precondition_error:
        raise HTTPException(status_code=400, detail=precondition_error)

    return await reprocess_book_images(book, db)


@router.delete("/{book_id}")
async def delete_book(
    book_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    import shutil

    result = await db.execute(
        select(Book).where(Book.id == uuid.UUID(book_id), Book.user_id == current_user.id)
    )
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if os.path.exists(book.file_path):
        os.remove(book.file_path)
    image_dir = os.path.join(settings.upload_dir, "images", str(book.id))
    if os.path.isdir(image_dir):
        shutil.rmtree(image_dir)
    await db.delete(book)
    await db.commit()
    return {"status": "deleted"}
