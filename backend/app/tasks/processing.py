import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from app.config import settings
from app.models.book import Book, BookStatus, Chapter, Section
from app.services.parser.pdf_parser import parse_pdf
from app.services.extractor.structure import extract_structure

logger = logging.getLogger(__name__)


async def _process_book(book_id: str):
    # Create a fresh engine for this event loop (background thread has its own loop)
    engine = create_async_engine(settings.database_url, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as db:
        result = await db.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            return

        try:
            # Step 1: Parse the file
            book.status = BookStatus.parsing
            await db.commit()

            if book.file_type == "pdf":
                parsed = parse_pdf(book.file_path)
                book.title = parsed.title or book.title
                book.author = parsed.author or book.author
                book.total_pages = parsed.total_pages
                await db.commit()
            else:
                book.status = BookStatus.error
                book.error_message = f"Unsupported file type: {book.file_type}"
                await db.commit()
                return

            # Step 2: Extract structure (chapters + sections) via LLM
            book.status = BookStatus.extracting
            await db.commit()

            structure = await extract_structure(parsed)

            # Update book metadata from LLM if better
            if structure.get("title") and not parsed.title:
                book.title = structure["title"]
            if structure.get("author") and not parsed.author:
                book.author = structure["author"]

            # Create chapters and sections in the database
            # KP extraction is deferred to when user starts studying a section
            for ch_data in structure.get("chapters", []):
                chapter = Chapter(
                    book_id=book.id,
                    title=ch_data["title"],
                    order_index=ch_data.get("order_index", 0),
                )
                db.add(chapter)
                await db.flush()

                for sec_data in ch_data.get("sections", []):
                    section = Section(
                        chapter_id=chapter.id,
                        title=sec_data["title"],
                        order_index=sec_data.get("order_index", 0),
                        content_raw=sec_data.get("content", ""),
                    )
                    db.add(section)

            book.status = BookStatus.ready
            await db.commit()

            logger.info("Book '%s' processed successfully (structure only, KPs deferred)", book.title)

        except Exception as e:
            logger.error("Book processing failed for %s: %s", book_id, e)
            book.status = BookStatus.error
            book.error_message = str(e)
            await db.commit()

    await engine.dispose()


def process_book(book_id: str):
    """Sync wrapper for FastAPI BackgroundTasks."""
    asyncio.run(_process_book(book_id))
