import os
import uuid
from dataclasses import dataclass, field

import fitz  # PyMuPDF

from app.config import settings


@dataclass
class PageImage:
    """An image extracted from a PDF page."""
    image_path: str       # absolute path on disk
    image_url: str        # relative URL for serving, e.g. /api/images/<book_id>/<filename>
    page_number: int
    index_on_page: int    # 0-based index among images on this page
    width: int
    height: int


@dataclass
class ParsedPage:
    page_number: int
    text: str
    images: list[PageImage] = field(default_factory=list)


@dataclass
class ParsedBook:
    title: str
    author: str
    total_pages: int
    pages: list[ParsedPage]
    toc: list[tuple[int, str, int]]  # (level, title, page)
    images: list[PageImage] = field(default_factory=list)


# Minimum dimensions to filter out tiny decorative images (icons, bullets, etc.)
MIN_IMAGE_WIDTH = 50
MIN_IMAGE_HEIGHT = 50
# Minimum byte size to skip trivial images
MIN_IMAGE_BYTES = 2048


def _extract_page_images(
    doc: fitz.Document,
    page: fitz.Page,
    page_number: int,
    image_dir: str,
    book_id: str,
) -> list[PageImage]:
    """Extract meaningful images from a single PDF page."""
    images = []
    image_list = page.get_images(full=True)

    for img_idx, img_info in enumerate(image_list):
        xref = img_info[0]
        try:
            base_image = doc.extract_image(xref)
        except Exception:
            continue

        if not base_image or not base_image.get("image"):
            continue

        width = base_image.get("width", 0)
        height = base_image.get("height", 0)
        image_bytes = base_image["image"]

        # Filter out tiny / trivial images
        if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
            continue
        if len(image_bytes) < MIN_IMAGE_BYTES:
            continue

        ext = base_image.get("ext", "png")
        filename = f"p{page_number}_img{img_idx}_{uuid.uuid4().hex[:8]}.{ext}"
        image_path = os.path.join(image_dir, filename)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        image_url = f"/api/images/{book_id}/{filename}"

        images.append(PageImage(
            image_path=image_path,
            image_url=image_url,
            page_number=page_number,
            index_on_page=img_idx,
            width=width,
            height=height,
        ))

    return images


def parse_pdf(file_path: str, book_id: str | None = None) -> ParsedBook:
    doc = fitz.open(file_path)

    title = doc.metadata.get("title", "") or ""
    author = doc.metadata.get("author", "") or ""

    # Set up image output directory
    if book_id:
        image_dir = os.path.join(settings.upload_dir, "images", book_id)
        os.makedirs(image_dir, exist_ok=True)
    else:
        image_dir = None

    all_images: list[PageImage] = []
    pages = []
    for i, page in enumerate(doc):
        page_number = i + 1
        text = page.get_text("text")

        # Extract images if we have an output directory
        page_images: list[PageImage] = []
        if image_dir:
            page_images = _extract_page_images(doc, page, page_number, image_dir, book_id)
            all_images.extend(page_images)

        if text.strip() or page_images:
            pages.append(ParsedPage(page_number=page_number, text=text, images=page_images))

    toc = [(level, title, page) for level, title, page in doc.get_toc()]
    total_pages = len(doc)
    doc.close()

    return ParsedBook(
        title=title,
        author=author,
        total_pages=total_pages,
        pages=pages,
        toc=toc,
        images=all_images,
    )
