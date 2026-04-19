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
import re
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


def parse_comprehension_verdict(text: str) -> tuple[str, str, str | None]:
    """Strip a trailing verdict marker.

    Returns ``(cleaned_text, action, verdict)`` where ``action`` is
    ``"continue"`` on UNDERSTOOD else ``"pause"``, and ``verdict`` is
    ``"UNDERSTOOD"`` / ``"CLARIFY"`` / ``None`` (no marker).
    """
    stripped = text.rstrip()
    for marker, action, verdict in (
        (_VERDICT_UNDERSTOOD, "continue", "UNDERSTOOD"),
        (_VERDICT_CLARIFY, "pause", "CLARIFY"),
    ):
        if stripped.endswith(marker):
            return stripped[: -len(marker)].rstrip(), action, verdict
    return text, "pause", None


# ── Profile-note marker parsing ────────────────────────────────
#
# The tutor optionally emits `<<PROFILE_NOTE: one sentence.>>` when it
# learns something durable about the student. Parsed post-stream: the
# VerdictStreamFilter only hides trailing verdict markers, not notes.
# A brief visual flicker of the note at end-of-stream is acceptable —
# the `done` event carries the cleaned text which the client renders as
# authoritative.

_PROFILE_NOTE_PATTERN = re.compile(r"<<PROFILE_NOTE:\s*(.+?)\s*>>", re.DOTALL)


def parse_profile_notes(text: str) -> tuple[str, list[str]]:
    """Extract all `<<PROFILE_NOTE: ...>>` markers.

    Returns ``(cleaned_text, notes)`` where ``notes`` is a list of note
    bodies (without markers) and ``cleaned_text`` has them removed.
    """
    notes: list[str] = []

    def _sub(match: "re.Match[str]") -> str:
        body = match.group(1).strip()
        if body:
            notes.append(body)
        return ""

    cleaned = _PROFILE_NOTE_PATTERN.sub(_sub, text)
    # Collapse any blank-line runs left behind by removal.
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).rstrip()
    return cleaned, notes


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
