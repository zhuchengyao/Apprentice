"""Convert PDF pages to semantic HTML using PyMuPDF's structured dict output."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from html import escape

import fitz

from app.services.parser.pdf_parser import PageImage, ParsedBook


@dataclass
class HtmlConversionResult:
    page_number: int
    html: str


# Span flag bits (PyMuPDF)
FLAG_SUPERSCRIPT = 1
FLAG_ITALIC = 2
FLAG_MONOSPACE = 8
FLAG_BOLD = 16

# Heading detection
HEADING_SIZE_RATIO = 1.2  # font size >= body * ratio → heading candidate
MAX_HEADING_LEVELS = 6

# List patterns
_BULLET_RE = re.compile(r'^[\u2022\u2023\u25CF\u25CB\u25AA\u25AB\u2013\u2014\-\*\u00B7]\s+')
_ORDERED_RE = re.compile(r'^(\d+)[.\)]\s+')
_LETTER_RE = re.compile(r'^([a-zA-Z])[.\)]\s+')


def _analyze_fonts(doc: fitz.Document) -> tuple[float, list[float]]:
    """Analyze font sizes across the entire document.

    Returns:
        body_size: the most common font size (by character count)
        heading_sizes: distinct sizes larger than body, sorted descending
    """
    size_chars: Counter[float] = Counter()

    for page in doc:
        text_dict = page.get_text("dict")
        for block in text_dict.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if text:
                        # Round to 1 decimal to group similar sizes
                        size = round(span.get("size", 0), 1)
                        size_chars[size] += len(text)

    if not size_chars:
        return 12.0, []

    body_size = size_chars.most_common(1)[0][0]

    # Collect heading candidate sizes
    threshold = body_size * HEADING_SIZE_RATIO
    heading_sizes = sorted(
        [s for s in size_chars if s >= threshold and s != body_size],
        reverse=True,
    )

    return body_size, heading_sizes


def _size_to_heading_level(size: float, heading_sizes: list[float]) -> int | None:
    """Map a font size to a heading level (1-6), or None if not a heading."""
    if size not in heading_sizes:
        return None
    idx = heading_sizes.index(size)
    return min(idx + 1, MAX_HEADING_LEVELS)


def _span_to_html(span: dict) -> str:
    """Convert a single span to inline HTML with formatting tags."""
    text = span.get("text", "")
    if not text:
        return ""

    html = escape(text)
    flags = span.get("flags", 0)

    if flags & FLAG_BOLD:
        html = f"<strong>{html}</strong>"
    if flags & FLAG_ITALIC:
        html = f"<em>{html}</em>"
    if flags & FLAG_SUPERSCRIPT:
        html = f"<sup>{html}</sup>"
    if flags & FLAG_MONOSPACE:
        html = f"<code>{html}</code>"

    return html


def _line_to_html(line: dict) -> str:
    """Convert all spans in a line to a single HTML string."""
    parts = []
    for span in line.get("spans", []):
        parts.append(_span_to_html(span))
    return "".join(parts)


def _get_line_font_size(line: dict) -> float:
    """Get the dominant font size for a line (longest span wins)."""
    best_size = 0.0
    best_len = 0
    for span in line.get("spans", []):
        text = span.get("text", "").strip()
        if len(text) > best_len:
            best_len = len(text)
            best_size = round(span.get("size", 0), 1)
    return best_size


def _get_line_text(line: dict) -> str:
    """Get plain text of a line."""
    return "".join(span.get("text", "") for span in line.get("spans", []))


def _detect_list_type(text: str) -> tuple[str | None, str]:
    """Detect if text starts with a list marker.

    Returns:
        (list_type, cleaned_text) where list_type is 'ul', 'ol', or None
    """
    m = _BULLET_RE.match(text)
    if m:
        return "ul", text[m.end():]

    m = _ORDERED_RE.match(text)
    if m:
        return "ol", text[m.end():]

    m = _LETTER_RE.match(text)
    if m:
        return "ol", text[m.end():]

    return None, text


def _match_image_block(
    block_bbox: tuple,
    page_images: list[PageImage],
    page: fitz.Page,
) -> PageImage | None:
    """Find the PageImage that best matches an image block's bounding box.

    Builds a mapping from image placement rects to PageImages, then picks
    the one with the largest overlap against the block bbox.
    """
    if not page_images:
        return None

    block_rect = fitz.Rect(block_bbox)

    # Build rect → PageImage mapping by correlating xref placement rects
    # with extracted PageImages via index order on the page.
    rect_to_image: list[tuple[fitz.Rect, PageImage]] = []

    # Collect all non-trivial image rects in document order
    page_area = page.rect.width * page.rect.height
    all_rects: list[fitz.Rect] = []
    for img_info in page.get_images(full=True):
        xref = img_info[0]
        try:
            for rect in page.get_image_rects(xref):
                if rect.is_empty or rect.is_infinite:
                    continue
                if rect.width * rect.height > page_area * 0.6:
                    continue  # skip full-page backgrounds
                all_rects.append(rect)
        except Exception:
            continue

    # Match extracted PageImages to rects by index_on_page
    for img in page_images:
        if img.index_on_page < len(all_rects):
            rect_to_image.append((all_rects[img.index_on_page], img))

    # Find best overlap
    best_match: PageImage | None = None
    best_overlap = 0.0
    for rect, img in rect_to_image:
        inter = block_rect & rect
        if not inter.is_empty:
            overlap = inter.width * inter.height
            if overlap > best_overlap:
                best_overlap = overlap
                best_match = img

    return best_match


def convert_page_to_html(
    page: fitz.Page,
    page_number: int,
    page_images: list[PageImage],
    body_size: float,
    heading_sizes: list[float],
) -> HtmlConversionResult:
    """Convert a single PDF page to semantic HTML.

    Args:
        page: PyMuPDF page object
        page_number: 1-based page number
        page_images: extracted PageImage objects for this page
        body_size: the document's body font size
        heading_sizes: sorted list of heading font sizes (largest first)
    """
    text_dict = page.get_text("dict")
    blocks = text_dict.get("blocks", [])
    html_parts: list[str] = []

    # Track which images we've already placed
    used_images: set[str] = set()

    for block in blocks:
        block_type = block.get("type", 0)

        # Image block
        if block_type == 1:
            matched = _match_image_block(block.get("bbox", ()), page_images, page)
            if matched and matched.image_url not in used_images:
                used_images.add(matched.image_url)
                html_parts.append(
                    f'<figure><img src="{escape(matched.image_url)}" '
                    f'alt="Figure from page {page_number}" loading="lazy"></figure>'
                )
            continue

        # Text block
        lines = block.get("lines", [])
        if not lines:
            continue

        # Process lines: accumulate paragraphs, detect headings and lists
        current_list_type: str | None = None
        current_list_items: list[str] = []
        paragraph_lines: list[str] = []

        def _flush_paragraph():
            if paragraph_lines:
                text = " ".join(paragraph_lines)
                if text.strip():
                    html_parts.append(f"<p>{text}</p>")
                paragraph_lines.clear()

        def _flush_list():
            nonlocal current_list_type
            if current_list_items:
                tag = current_list_type or "ul"
                items = "".join(f"<li>{item}</li>" for item in current_list_items)
                html_parts.append(f"<{tag}>{items}</{tag}>")
                current_list_items.clear()
            current_list_type = None

        for line in lines:
            line_html = _line_to_html(line)
            line_text = _get_line_text(line).strip()
            line_size = _get_line_font_size(line)

            if not line_text:
                continue

            # Check if this line is a heading
            heading_level = _size_to_heading_level(line_size, heading_sizes)
            if heading_level is not None:
                _flush_paragraph()
                _flush_list()
                html_parts.append(f"<h{heading_level}>{line_html}</h{heading_level}>")
                continue

            # Check for list items
            list_type, cleaned = _detect_list_type(line_text)
            if list_type:
                _flush_paragraph()
                if current_list_type and current_list_type != list_type:
                    _flush_list()
                current_list_type = list_type
                # Re-render the cleaned text with formatting
                # Use the full line HTML but strip the bullet/number marker
                item_html = line_html
                for pattern in [_BULLET_RE, _ORDERED_RE, _LETTER_RE]:
                    m = pattern.match(line_text)
                    if m:
                        # Remove the marker from the HTML too
                        marker = escape(line_text[:m.end()])
                        if item_html.startswith(marker):
                            item_html = item_html[len(marker):]
                        break
                current_list_items.append(item_html.strip() or escape(cleaned))
                continue

            # Regular paragraph line
            if current_list_type:
                _flush_list()
            paragraph_lines.append(line_html)

        _flush_paragraph()
        _flush_list()

    # Append any remaining images not placed via image blocks
    for img in page_images:
        if img.image_url not in used_images:
            html_parts.append(
                f'<figure><img src="{escape(img.image_url)}" '
                f'alt="Figure from page {page_number}" loading="lazy"></figure>'
            )

    return HtmlConversionResult(
        page_number=page_number,
        html="\n".join(html_parts),
    )


def convert_pages_to_html(
    file_path: str,
    parsed_pages: list["ParsedPage"],
    body_size: float | None = None,
    heading_sizes: list[float] | None = None,
) -> list[HtmlConversionResult]:
    """Convert a list of parsed pages to semantic HTML.

    If body_size/heading_sizes are not provided, they are computed from
    the full document for consistency.

    Args:
        file_path: path to the PDF (opened temporarily for dict extraction)
        parsed_pages: pages with text and extracted images
        body_size: pre-computed body font size (optional)
        heading_sizes: pre-computed heading sizes (optional)
    """
    from app.services.parser.pdf_parser import ParsedPage  # avoid circular at module level

    doc = fitz.open(file_path)

    if body_size is None or heading_sizes is None:
        body_size, heading_sizes = _analyze_fonts(doc)

    # Build page_number → images lookup
    page_images_map: dict[int, list[PageImage]] = {}
    for p in parsed_pages:
        if p.images:
            page_images_map[p.page_number] = p.images

    results: list[HtmlConversionResult] = []
    for p in parsed_pages:
        fitz_page = doc[p.page_number - 1]
        images = page_images_map.get(p.page_number, [])
        result = convert_page_to_html(fitz_page, p.page_number, images, body_size, heading_sizes)
        if result.html.strip():
            results.append(result)

    doc.close()
    return results


def convert_book_to_html(
    doc: fitz.Document,
    parsed_book: ParsedBook,
) -> list[HtmlConversionResult]:
    """Convert all pages of a PDF to semantic HTML.

    Args:
        doc: an open PyMuPDF document
        parsed_book: the ParsedBook with extracted images per page
    """
    body_size, heading_sizes = _analyze_fonts(doc)

    # Build page_number → images lookup
    page_images_map: dict[int, list[PageImage]] = {}
    for page in parsed_book.pages:
        if page.images:
            page_images_map[page.page_number] = page.images

    results: list[HtmlConversionResult] = []
    for i, page in enumerate(doc):
        page_number = i + 1
        images = page_images_map.get(page_number, [])
        result = convert_page_to_html(page, page_number, images, body_size, heading_sizes)
        if result.html.strip():
            results.append(result)

    return results
