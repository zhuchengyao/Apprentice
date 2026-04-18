"""Teaching agent — orchestrates knowledge-point-by-knowledge-point teaching.

The agent decides WHAT to teach; the AI decides HOW to teach it.

Pacing rules:
  - Lightweight KPs (short explanation, low difficulty) can be batched, but
    a batch never crosses a section boundary — sections are the author's
    topical groupings, batching across them muddles the narrative.
  - Heavy KPs (long explanation, high difficulty) are taught one at a time,
    followed by a pause for student questions.
  - After the last KP in a section, we pause so the student can take stock
    before the next section begins.
"""

import logging
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.book import Section, KnowledgePoint

logger = logging.getLogger(__name__)

HEAVY_EXPLANATION_THRESHOLD = 300
HEAVY_DIFFICULTY_THRESHOLD = 3
BATCH_MAX = 3


@dataclass
class TeachingStep:
    knowledge_points: list[KnowledgePoint]
    action: str  # "continue" | "pause"
    kp_end_index: int


async def get_chapter_knowledge_points(
    chapter_id, db: AsyncSession
) -> list[KnowledgePoint]:
    result = await db.execute(
        select(Section)
        .where(Section.chapter_id == chapter_id)
        .options(selectinload(Section.knowledge_points))
        .order_by(Section.order_index)
    )
    sections = result.scalars().all()
    kps = []
    for section in sections:
        for kp in sorted(section.knowledge_points, key=lambda k: k.order_index):
            kps.append(kp)
    return kps


def _is_heavy(kp: KnowledgePoint) -> bool:
    return (
        len(kp.explanation or "") > HEAVY_EXPLANATION_THRESHOLD
        or kp.difficulty >= HEAVY_DIFFICULTY_THRESHOLD
    )


def plan_next_step(
    all_kps: list[KnowledgePoint],
    current_index: int,
) -> TeachingStep | None:
    """Determine the next teaching step starting from current_index.

    Returns None if all knowledge points have been taught.
    """
    if current_index >= len(all_kps):
        return None

    kp = all_kps[current_index]

    if _is_heavy(kp):
        # Heavy KPs always stand alone and always pause.
        return TeachingStep(
            knowledge_points=[kp],
            action="pause",
            kp_end_index=current_index + 1,
        )

    # Batch lightweight KPs, but never across a section boundary.
    batch = [kp]
    i = current_index + 1
    while i < len(all_kps) and len(batch) < BATCH_MAX:
        next_kp = all_kps[i]
        if _is_heavy(next_kp):
            break
        if next_kp.section_id != kp.section_id:
            break
        batch.append(next_kp)
        i += 1

    # Decide whether to pause or continue based on what comes next.
    if i >= len(all_kps):
        # Last KP of the chapter — pause so we don't auto-advance into "done".
        action = "pause"
    elif all_kps[i].section_id != kp.section_id:
        # Crossing a section boundary — pause for a breath.
        action = "pause"
    elif _is_heavy(all_kps[i]):
        # Next KP is heavy — pause so the student is fresh for it.
        action = "pause"
    else:
        action = "continue"

    return TeachingStep(
        knowledge_points=batch,
        action=action,
        kp_end_index=i,
    )


def format_kp_list(kps: list[KnowledgePoint]) -> str:
    """Format all knowledge points as a numbered list for the system prompt."""
    lines = []
    for i, kp in enumerate(kps):
        diff = "easy" if kp.difficulty <= 1 else "medium" if kp.difficulty <= 2 else "hard"
        lines.append(f"{i + 1}. [{diff}] {kp.concept}: {kp.explanation[:120]}...")
    return "\n".join(lines) if lines else "(no knowledge points)"


# ── Comprehension marker parsing ───────────────────────────────

# The answer prompt instructs the model to end its reply with one of these
# markers when the student was responding to a Socratic question. We strip
# the marker before saving the message and use it to set the SSE action.
_VERDICT_UNDERSTOOD = "<<UNDERSTOOD>>"
_VERDICT_CLARIFY = "<<CLARIFY>>"
_VERDICT_MARKERS = (_VERDICT_UNDERSTOOD, _VERDICT_CLARIFY)
_VERDICT_TAIL_LEN = max(len(m) for m in _VERDICT_MARKERS)


def parse_comprehension_verdict(text: str) -> tuple[str, str]:
    """Strip a trailing verdict marker and return (cleaned_text, action).

    action is "continue" if the model judged the student understood, else
    "pause". If no marker is present, action defaults to "pause".
    """
    stripped = text.rstrip()
    for marker, action in (
        (_VERDICT_UNDERSTOOD, "continue"),
        (_VERDICT_CLARIFY, "pause"),
    ):
        if stripped.endswith(marker):
            return stripped[: -len(marker)].rstrip(), action
    return text, "pause"


class VerdictStreamFilter:
    """Streaming filter that holds back trailing characters which might be
    forming a verdict marker, so the user never sees the marker flash.

    Usage:
        f = VerdictStreamFilter()
        async for chunk in stream:
            safe = f.push(chunk)   # may be empty while buffering a "<<..."
            if safe: yield safe
        final_tail = f.flush()      # remaining non-marker tail
        cleaned, action = parse_comprehension_verdict(full_text)
    """

    def __init__(self) -> None:
        self._buf = ""

    def push(self, chunk: str) -> str:
        """Accept a new chunk; return the portion safe to emit now."""
        self._buf += chunk
        # Hold back the last _VERDICT_TAIL_LEN chars. Anything before that
        # can't be part of a trailing marker.
        if len(self._buf) <= _VERDICT_TAIL_LEN:
            return ""
        safe_end = len(self._buf) - _VERDICT_TAIL_LEN
        out = self._buf[:safe_end]
        self._buf = self._buf[safe_end:]
        return out

    def flush(self) -> str:
        """Return the tail buffer minus any trailing marker."""
        stripped = self._buf.rstrip()
        for marker in _VERDICT_MARKERS:
            if stripped.endswith(marker):
                return stripped[: -len(marker)].rstrip()
        tail = self._buf
        self._buf = ""
        return tail
