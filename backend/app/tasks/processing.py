import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from app.config import settings
from app.models.book import Book, BookStatus, Chapter, Section
from app.services.parser.pdf_parser import parse_pdf, ParsedBook
from app.services.extractor.structure import extract_structure

logger = logging.getLogger(__name__)


def _extract_phrases(text: str, phrase_len: int = 30, count: int = 8) -> list[str]:
    """Extract several short phrases from different positions in the text for fuzzy matching."""
    import re
    # Clean whitespace, collapse runs
    cleaned = re.sub(r'\s+', ' ', text.strip())
    if len(cleaned) < phrase_len:
        return [cleaned] if len(cleaned) > 15 else []

    phrases = []
    # Sample from evenly spaced positions across the text
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
    phrases = _extract_phrases(page_text)
    if not phrases:
        return False
    # If any phrase from the page appears in the section, it's a match
    for phrase in phrases:
        if phrase in section_content:
            return True

    # Fallback: check significant word overlap
    import re
    page_words = set(w.lower() for w in re.findall(r'[a-zA-Z]{5,}', page_text))
    section_words = set(w.lower() for w in re.findall(r'[a-zA-Z]{5,}', section_content))
    if not page_words:
        return False
    overlap = len(page_words & section_words) / len(page_words)
    return overlap > 0.4


def _inject_images_into_sections(parsed: ParsedBook, structure: dict) -> None:
    """Post-process: inject image refs into section content by matching page text.

    The structure extractor LLM doesn't reliably preserve image refs, so we
    match each section's content against page texts and append relevant images.
    Uses multiple matching strategies: short phrase matching and word overlap.
    """
    if not parsed.images:
        return

    # Build page_number → list of image markdown refs
    page_images: dict[int, list[str]] = {}
    for img in parsed.images:
        page_images.setdefault(img.page_number, []).append(img.image_url)

    # Build page_number → full text for matching
    page_texts: dict[int, str] = {}
    for page in parsed.pages:
        text = page.text.strip()
        if text:
            page_texts[page.page_number] = text

    for ch_data in structure.get("chapters", []):
        for sec_data in ch_data.get("sections", []):
            content = sec_data.get("content", "")
            if not content:
                continue

            # Skip if images are already embedded (LLM preserved them)
            if "/api/images/" in content:
                continue

            matched_images: list[str] = []
            for page_num in sorted(page_images.keys()):
                if page_num not in page_texts:
                    continue
                if _page_matches_section(page_texts[page_num], content):
                    for url in page_images[page_num]:
                        matched_images.append(
                            f"![Figure from page {page_num}]({url})"
                        )

            if matched_images:
                sec_data["content"] = (
                    content + "\n\n" + "\n\n".join(matched_images)
                )


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
                parsed = parse_pdf(book.file_path, book_id=str(book.id))
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

            # Step 2.5: Inject image refs into section content
            _inject_images_into_sections(parsed, structure)

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
