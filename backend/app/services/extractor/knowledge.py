import json
import logging

from app.services.ai_client import chat_completion

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

Return valid JSON only, no markdown fencing:
{
  "knowledge_points": [
    {
      "concept": "Concept name",
      "explanation": "Clear explanation of this concept...",
      "difficulty": 2,
      "order_index": 0
    }
  ],
  "section_summary": "A 1-2 sentence summary of what this section covers."
}
"""


async def extract_knowledge_points(section_title: str, section_content: str) -> dict:
    """
    Use Claude to extract knowledge points from a section's content.
    Returns dict with knowledge_points list and section_summary.
    """
    # Truncate very long sections
    content = section_content[:30000]

    response_text = await chat_completion(
        messages=[
            {
                "role": "user",
                "content": (
                    f"{KP_EXTRACTION_PROMPT}\n\n"
                    f"Section title: {section_title}\n\n"
                    f"Section content:\n{content}"
                ),
            }
        ],
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
