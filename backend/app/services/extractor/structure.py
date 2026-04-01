import json
import logging

from app.services.ai_client import chat_completion
from app.services.parser.pdf_parser import ParsedBook

logger = logging.getLogger(__name__)

STRUCTURE_PROMPT = """\
You are analyzing a book to extract its structure. Given the text content and optional table of contents, \
identify the chapters and sections.

Rules:
- Each chapter should have a title and contain 1+ sections.
- Each section is a coherent unit of content (a subchapter, a topic, or a logical division).
- If there is no clear chapter structure, create logical groupings by topic.
- Keep chapter/section titles concise but descriptive.
- For each section, include the raw text content that belongs to it.

Return valid JSON only, no markdown fencing:
{
  "title": "Book title (extracted or inferred)",
  "author": "Author name if detectable, otherwise empty string",
  "chapters": [
    {
      "title": "Chapter title",
      "order_index": 0,
      "sections": [
        {
          "title": "Section title",
          "order_index": 0,
          "content": "The full text content of this section..."
        }
      ]
    }
  ]
}
"""


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
        page_text = f"\n--- Page {page.page_number} ---\n{page.text}"
        if total_chars + len(page_text) > max_chars:
            parts.append(f"\n[... truncated at page {page.page_number}, {parsed.total_pages - page.page_number} pages remaining ...]")
            break
        parts.append(page_text)
        total_chars += len(page_text)

    return "\n".join(parts)


async def extract_structure(parsed: ParsedBook) -> dict:
    """
    Use Claude to extract chapter/section structure from a parsed book.
    Returns the structured dict with chapters and sections.
    """
    book_text = _build_book_text(parsed)

    response_text = await chat_completion(
        messages=[
            {
                "role": "user",
                "content": f"{STRUCTURE_PROMPT}\n\nHere is the book:\n\n{book_text}",
            }
        ],
        max_tokens=8192,
    )

    # Handle potential markdown fencing
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        # Remove first and last lines (fences)
        lines = [l for l in lines if not l.strip().startswith("```")]
        response_text = "\n".join(lines)

    try:
        structure = json.loads(response_text)
    except json.JSONDecodeError:
        logger.error("Failed to parse structure JSON from LLM response")
        # Fallback: create a single chapter with one section containing all content
        all_text = "\n\n".join(p.text for p in parsed.pages)
        structure = {
            "title": parsed.title or "Untitled",
            "author": parsed.author or "",
            "chapters": [
                {
                    "title": "Chapter 1",
                    "order_index": 0,
                    "sections": [
                        {
                            "title": "Full Content",
                            "order_index": 0,
                            "content": all_text[:50000],
                        }
                    ],
                }
            ],
        }

    return structure
