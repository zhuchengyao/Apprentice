"""Post-stream signal persistence for tutor turns.

After a tutor stream finishes we have three kinds of signals to persist:
KP exposures (for mastery decay), comprehension verdicts (understood vs.
clarify), and learner profile notes the model chose to record. Keeping
these bundled in one helper prevents the caller from forgetting one.
"""

from __future__ import annotations

import uuid

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import MAX_LEARNER_PROFILE_CHARS
from app.models.tutor import TutorConversation
from app.models.user import User
from app.services.learning.mastery import (
    QUALITY_CLARIFY,
    QUALITY_UNDERSTOOD,
    record_kp_exposure,
    update_mastery,
)


def merge_profile_notes(existing: str | None, notes: list[str]) -> str:
    """Append new notes to the existing profile, dedup, cap size."""
    lines = [ln.rstrip() for ln in (existing or "").splitlines() if ln.strip()]
    existing_lower = {ln.lower().lstrip("- ").strip() for ln in lines}
    for note in notes:
        key = note.lower().strip()
        if not key or key in existing_lower:
            continue
        lines.append(f"- {note}")
        existing_lower.add(key)
    merged = "\n".join(lines)
    while len(merged) > MAX_LEARNER_PROFILE_CHARS and len(lines) > 1:
        lines.pop(0)
        merged = "\n".join(lines)
    return merged


async def apply_post_stream_signals(
    save_db: AsyncSession,
    user_id: uuid.UUID,
    conv_id: uuid.UUID,
    profile_notes: list[str],
    verdict_kp_id: uuid.UUID | None,
    verdict: str | None,
    exposed_kp_ids: list[uuid.UUID],
) -> None:
    """Apply mastery + profile updates after a tutor stream completes.

    Caller is responsible for commit.
    """
    for kp_id in exposed_kp_ids:
        await record_kp_exposure(save_db, user_id, kp_id)

    if verdict_kp_id is not None and verdict is not None:
        quality = QUALITY_UNDERSTOOD if verdict == "UNDERSTOOD" else QUALITY_CLARIFY
        await update_mastery(save_db, user_id, verdict_kp_id, quality)

    if profile_notes:
        user_obj = await save_db.get(User, user_id)
        if user_obj is not None:
            user_obj.learner_profile = merge_profile_notes(
                user_obj.learner_profile, profile_notes
            )
        # Invalidate student-block cache on all this user's conversations
        # so the next turn picks up the updated profile.
        await save_db.execute(
            update(TutorConversation)
            .where(TutorConversation.user_id == user_id)
            .values(student_block_cache=None)
        )
