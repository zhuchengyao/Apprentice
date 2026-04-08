import json
import logging
from dataclasses import dataclass

from app.services.ai_client import chat_completion
from app.services.teaching.prompts import EVALUATE_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


@dataclass
class AssessmentResult:
    quality: int  # 0-5 SM-2 scale
    feedback: str


async def assess_response(
    student_response: str,
    concept: str,
    explanation: str,
    question: str,
) -> AssessmentResult:
    """Use the AI to evaluate a student's response and return a quality score + feedback."""
    prompt = EVALUATE_SYSTEM_PROMPT.format(
        concept=concept,
        explanation=explanation,
        question=question,
        student_response=student_response,
    )

    response_text = await chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        caller="assessment",
    )

    # Strip markdown fencing if present
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        response_text = "\n".join(lines)

    try:
        result = json.loads(response_text)
        quality = max(0, min(5, int(result.get("quality", 2))))
        feedback = result.get("feedback", "Let's try another approach.")
    except (json.JSONDecodeError, ValueError):
        logger.warning("Failed to parse assessment JSON: %s", response_text)
        quality = 2
        feedback = response_text if len(response_text) < 500 else "Let's try another approach."

    return AssessmentResult(quality=quality, feedback=feedback)
