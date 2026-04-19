"""Re-extract figures from a book's PDF and stitch them back onto sections.

Used by `POST /books/{id}/reprocess-images` after the image pipeline
evolves. Sections' existing KPs are cleared so they get regenerated with
figure-awareness on next study — we can't retrofit figures into old
text-only KPs without re-prompting anyway.
"""

from __future__ import annotations

import asyncio
import os

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book
from app.services.matching import page_matches_section
from app.services.parser.pdf_parser import parse_pdf


_FIGURES_MARKER = "\n\n---\n## Book Figures\n"


async def reprocess_book_images(book: Book, db: AsyncSession) -> dict:
    """Re-extract images + rewrite section content_raw with figure refs.

    Caller must have already loaded `book.chapters → sections → knowledge_points`
    and validated that the PDF exists on disk.
    """
    loop = asyncio.get_running_loop()
    parsed = await loop.run_in_executor(
        None, lambda: parse_pdf(book.file_path, book_id=str(book.id))
    )

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
            if _FIGURES_MARKER in raw:
                raw = raw[: raw.index(_FIGURES_MARKER)]

            matched: list[str] = []
            for page_num in sorted(page_images.keys()):
                if page_num not in page_texts:
                    continue
                if page_matches_section(page_texts[page_num], raw):
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
        "message": (
            f"Extracted {total_images} images. Deleted {kps_deleted} KPs — "
            "they will be re-generated with figure awareness on next study."
        ),
    }


def validate_reprocess_preconditions(book: Book) -> str | None:
    """Return a human-readable error string if `book` can't be reprocessed,
    or None if it's OK. The caller translates this into an HTTPException.
    """
    if book.file_type != "pdf":
        return "Only PDF books can be reprocessed"
    if not os.path.exists(book.file_path):
        return "PDF file not found on disk"
    return None
