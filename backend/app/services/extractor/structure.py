import json
import logging

from app.services.ai_client import chat_completion
from app.services.parser.pdf_parser import ParsedBook, ParsedPage

logger = logging.getLogger(__name__)

# Two-pass approach: first extract outline (titles + page ranges), then assign content.
# This avoids asking the LLM to repeat book content — which fails for large books.

OUTLINE_PROMPT = """\
You are analyzing a book to extract its chapter and section structure. \
Given the text content and optional table of contents, identify every chapter and section \
with the page numbers where each begins.

Rules:
- Each chapter should have a title and contain 1 or more sections.
- Each section is a coherent unit of content (a subchapter, a topic, or a logical division).
- If there is no clear chapter structure, create logical groupings by topic.
- Keep chapter/section titles concise but descriptive.
- For each chapter and section, provide the page number where it starts.
- Do NOT include the actual content text — only titles and page numbers.
- Order chapters and sections by their appearance in the book.

Return valid JSON only, no markdown fencing:
{
  "title": "Book title (extracted or inferred)",
  "author": "Author name if detectable, otherwise empty string",
  "chapters": [
    {
      "title": "Chapter title",
      "start_page": 1,
      "sections": [
        {
          "title": "Section title",
          "start_page": 1
        }
      ]
    }
  ]
}
"""


def _build_page_text(page: ParsedPage) -> str:
    """Build text for a single page, interleaving text and image references."""
    parts = [page.text]
    if page.images:
        for img in page.images:
            parts.append(f"\n![Figure from page {page.page_number}]({img.image_url})")
    return "\n".join(parts)


def _build_book_text(parsed: ParsedBook, max_chars: int = 150000) -> str:
    """Build a text representation of the book for the LLM, truncated to fit context."""
    parts = []

    if parsed.toc:
        parts.append("=== TABLE OF CONTENTS ===")
        for level, title, page in parsed.toc:
            indent = "  " * (level - 1)
            parts.append(f"{indent}- {title} (page {page})")
        parts.append("")

    parts.append("=== BOOK CONTENT ===")
    total_chars = sum(len(p) for p in parts)

    for page in parsed.pages:
        page_content = _build_page_text(page)
        page_text = f"\n--- Page {page.page_number} ---\n{page_content}"
        if total_chars + len(page_text) > max_chars:
            parts.append(f"\n[... truncated at page {page.page_number}, {parsed.total_pages - page.page_number} pages remaining ...]")
            break
        parts.append(page_text)
        total_chars += len(page_text)

    return "\n".join(parts)


def _assign_content_to_sections(parsed: ParsedBook, outline: dict) -> dict:
    """Assign page content to sections based on the outline's page ranges.

    This is the second pass: we take the LLM's outline (titles + start pages)
    and programmatically fill in each section's content from the parsed pages.
    Images are included automatically via _build_page_text.
    """
    # Build page lookup: page_number → page object
    page_map: dict[int, ParsedPage] = {p.page_number: p for p in parsed.pages}

    # Collect all section boundaries as (chapter_idx, section_idx, start_page)
    boundaries: list[tuple[int, int, int]] = []
    chapters = outline.get("chapters", [])
    for ch_idx, ch in enumerate(chapters):
        for sec_idx, sec in enumerate(ch.get("sections", [])):
            boundaries.append((ch_idx, sec_idx, sec.get("start_page", 1)))

    # Sort by start_page
    boundaries.sort(key=lambda b: b[2])

    # Determine end_page for each section (= start of next section - 1, or last page)
    last_page = parsed.total_pages
    section_ranges: list[tuple[int, int, int, int]] = []  # (ch_idx, sec_idx, start, end)
    for i, (ch_idx, sec_idx, start) in enumerate(boundaries):
        if i + 1 < len(boundaries):
            end = boundaries[i + 1][2] - 1
        else:
            end = last_page
        section_ranges.append((ch_idx, sec_idx, start, end))

    # Build content for each section
    for ch_idx, sec_idx, start, end in section_ranges:
        content_parts = []
        for pg_num in range(start, end + 1):
            page = page_map.get(pg_num)
            if page:
                content_parts.append(_build_page_text(page))
        content = "\n\n".join(content_parts)
        chapters[ch_idx]["sections"][sec_idx]["content"] = content
        chapters[ch_idx]["sections"][sec_idx]["order_index"] = sec_idx

    # Set chapter order_index
    for ch_idx, ch in enumerate(chapters):
        ch["order_index"] = ch_idx

    return outline


def _parse_llm_json(response_text: str) -> dict | None:
    """Try to parse JSON from LLM response, handling markdown fencing."""
    text = response_text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _fallback_from_toc(parsed: ParsedBook) -> dict:
    """Build structure from the PDF's table of contents if available."""
    if not parsed.toc:
        return _fallback_single_sections(parsed)

    chapters: list[dict] = []
    current_chapter: dict | None = None

    for level, title, page in parsed.toc:
        if level == 1:
            current_chapter = {"title": title, "start_page": page, "sections": []}
            chapters.append(current_chapter)
        elif level >= 2 and current_chapter:
            current_chapter["sections"].append({"title": title, "start_page": page})

    # If TOC only has level-1 entries, treat each as a chapter with one section
    for ch in chapters:
        if not ch["sections"]:
            ch["sections"].append({"title": ch["title"], "start_page": ch["start_page"]})

    if not chapters:
        return _fallback_single_sections(parsed)

    outline = {
        "title": parsed.title or "Untitled",
        "author": parsed.author or "",
        "chapters": chapters,
    }
    return _assign_content_to_sections(parsed, outline)


def _fallback_single_sections(parsed: ParsedBook) -> dict:
    """Last resort: split book into chunks of ~20 pages each."""
    chunk_size = 20
    sections = []
    page_map = {p.page_number: p for p in parsed.pages}
    page_numbers = sorted(page_map.keys())

    for i in range(0, len(page_numbers), chunk_size):
        chunk_pages = page_numbers[i:i + chunk_size]
        start, end = chunk_pages[0], chunk_pages[-1]
        content_parts = [_build_page_text(page_map[pn]) for pn in chunk_pages]
        sections.append({
            "title": f"Pages {start}–{end}",
            "order_index": len(sections),
            "content": "\n\n".join(content_parts),
        })

    return {
        "title": parsed.title or "Untitled",
        "author": parsed.author or "",
        "chapters": [
            {
                "title": "Content",
                "order_index": 0,
                "sections": sections,
            }
        ],
    }


async def extract_structure(parsed: ParsedBook) -> dict:
    """Extract chapter/section structure from a parsed book.

    Uses a two-pass approach:
    1. LLM extracts an outline (titles + page ranges) — small output, reliable
    2. Content is assigned to sections programmatically from parsed pages
    """
    book_text = _build_book_text(parsed)

    response_text = await chat_completion(
        messages=[
            {
                "role": "user",
                "content": f"{OUTLINE_PROMPT}\n\nHere is the book:\n\n{book_text}",
            }
        ],
        max_tokens=8192,
        caller="structure_extraction",
    )

    outline = _parse_llm_json(response_text)

    if not outline or not outline.get("chapters"):
        logger.warning("LLM outline extraction failed, falling back to TOC/chunking")
        return _fallback_from_toc(parsed)

    # Validate that sections have start_page
    valid = True
    for ch in outline.get("chapters", []):
        for sec in ch.get("sections", []):
            if "start_page" not in sec:
                valid = False
                break
        if not valid:
            break

    if not valid:
        logger.warning("LLM outline missing start_page values, falling back to TOC/chunking")
        return _fallback_from_toc(parsed)

    # Pass 2: assign content from pages
    structure = _assign_content_to_sections(parsed, outline)
    logger.info(
        "Structure extracted: %d chapters, %d total sections",
        len(structure.get("chapters", [])),
        sum(len(ch.get("sections", [])) for ch in structure.get("chapters", [])),
    )
    return structure
