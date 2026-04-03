import json
import logging
import re

from app.services.ai_client import chat_completion, build_image_content_blocks
from app.config import settings

logger = logging.getLogger(__name__)

KP_EXTRACTION_PROMPT = """\
You are analyzing a section of a book to extract discrete knowledge points.

A knowledge point is a single concept, fact, principle, or skill that a student should learn. \
Each knowledge point should be atomic — it teaches exactly one thing.

For the given section text, identify 3-10 knowledge points.

Rules:
- Each knowledge point has a concise concept name (max 80 chars).
- The explanation should be clear and self-contained (2-5 sentences), like a textbook definition.
- Difficulty is 1-5: 1=basic vocabulary/fact, 2=simple concept, 3=moderate concept requiring some background, \
4=complex concept with multiple parts, 5=advanced concept requiring synthesis.
- Order them from most foundational to most advanced.
- SKIP metadata: Do NOT create knowledge points about book titles, authors, publishers, ISBN numbers, \
copyright info, edition details, acknowledgments, table of contents, or any other publication metadata. \
Only extract knowledge points about the actual subject matter being taught.
- IMPORTANT — Image association: If the content contains image references like ![Figure ...](/api/images/...), \
determine which images are directly relevant to each knowledge point. For each KP, include an "image_refs" \
field containing a list of the relevant image URL paths (just the /api/images/... part, not the full \
markdown syntax). Only associate images that genuinely illustrate the specific concept — do not associate \
all images with every KP. Use an empty list [] if no images are relevant. Max 5 images per KP.
- You may also mention figures in the explanation text itself for context.
- For math expressions, use $...$ for inline math and $$...$$ for display math.

Return valid JSON only, no markdown fencing:
{
  "knowledge_points": [
    {
      "concept": "Concept name",
      "explanation": "Clear explanation of this concept...",
      "difficulty": 2,
      "order_index": 0,
      "image_refs": ["/api/images/book_id/filename.png"]
    }
  ],
  "section_summary": "A 1-2 sentence summary of what this section covers."
}
"""


def _extract_image_paths_from_content(content: str) -> list[str]:
    """Find image URLs in markdown content and resolve to local file paths."""
    # Match ![...]( /api/images/<book_id>/<filename> )
    pattern = r'!\[[^\]]*\]\(/api/images/([^/]+)/([^)]+)\)'
    paths = []
    for match in re.finditer(pattern, content):
        book_id, filename = match.group(1), match.group(2)
        import os
        path = os.path.join(settings.upload_dir, "images", book_id, filename)
        if os.path.isfile(path):
            paths.append(path)
    return paths


async def extract_knowledge_points(section_title: str, section_content: str) -> dict:
    """
    Use Claude to extract knowledge points from a section's content.
    Returns dict with knowledge_points list and section_summary.
    """
    # Truncate very long sections
    content = section_content[:30000]

    # Build message content — include images if present
    image_paths = _extract_image_paths_from_content(content)
    text_content = (
        f"{KP_EXTRACTION_PROMPT}\n\n"
        f"Section title: {section_title}\n\n"
        f"Section content:\n{content}"
    )

    if image_paths:
        # Build multimodal message with images
        content_blocks: list[dict] = [{"type": "text", "text": text_content}]
        content_blocks.extend(build_image_content_blocks(image_paths[:10]))  # cap at 10 images
        message_content: str | list[dict] = content_blocks
    else:
        message_content = text_content

    response_text = await chat_completion(
        messages=[{"role": "user", "content": message_content}],
        max_tokens=4096,
    )

    if response_text.startswith("```"):
        lines = response_text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        response_text = "\n".join(lines)

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        logger.error("Failed to parse KP JSON from LLM response for section: %s", section_title)
        result = {
            "knowledge_points": [
                {
                    "concept": section_title,
                    "explanation": f"Key concepts from: {section_title}",
                    "difficulty": 2,
                    "order_index": 0,
                }
            ],
            "section_summary": f"Content about {section_title}.",
        }

    return result
