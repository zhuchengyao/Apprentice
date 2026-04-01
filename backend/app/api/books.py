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
                )
                for kp in section.knowledge_points
            ]
            total_kps += len(kps)
            sections_resp.append(
                SectionResponse(
                    id=str(section.id),
                    chapter_id=str(section.chapter_id),
                    title=section.title,
                    order_index=section.order_index,
                    summary=section.summary,
                    knowledge_points=kps,
                )
            )
        chapters_resp.append(
            ChapterResponse(
                id=str(chapter.id),
                book_id=str(chapter.book_id),
                title=chapter.title,
                order_index=chapter.order_index,
                summary=chapter.summary,
                sections=sections_resp,
            )
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
