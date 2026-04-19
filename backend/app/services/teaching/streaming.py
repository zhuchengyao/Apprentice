"""Helpers shared by tutor + study SSE endpoints.

Each streaming endpoint had two near-identical try/except blocks: one
around the LLM stream call (→ TutorLLMError), one around the post-stream
DB persist (→ TutorPersistError). The wrappers below centralize that so
endpoint bodies focus on what's actually unique (filters, persist logic,
done payload).
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from app.services.ai_client import chat_completion_stream
from app.services.teaching.errors import (
    TutorLLMError,
    TutorPersistError,
    log_stream_failure,
    stream_error_payload,
)

logger = logging.getLogger(__name__)


async def iter_llm_chunks(**kwargs: Any) -> AsyncIterator[str]:
    """Wrap chat_completion_stream so upstream failures become TutorLLMError.

    GeneratorExit (raised when the consumer stops iterating) is BaseException-
    derived and intentionally not converted — it signals normal shutdown.
    """
    try:
        async for chunk in chat_completion_stream(**kwargs):
            yield chunk
    except Exception as e:
        raise TutorLLMError() from e


@asynccontextmanager
async def save_session():
    """Open a fresh DB session for post-stream persistence.

    Any failure inside the block is reraised as TutorPersistError so the
    SSE error event surfaces the right `kind` to the client.
    """
    # Local import: app.database imports models which import this package's
    # siblings, so importing at module load would risk a circular chain.
    from app.database import async_session

    try:
        async with async_session() as save_db:
            yield save_db
    except Exception as e:
        raise TutorPersistError() from e


async def wrap_sse_errors(
    caller: str,
    body: AsyncIterator[dict],
) -> AsyncIterator[dict]:
    """Forward SSE events from `body`; convert exceptions to an error event.

    Every tutor/study SSE endpoint had the same 3-line trailer:
        except Exception as e:
            log_stream_failure(logger, caller, e)
            yield {"event": "error", "data": stream_error_payload(e)}
    Centralizing here keeps the error contract (kind + client_message)
    identical across endpoints and preserves stack traces in logs.
    """
    try:
        async for event in body:
            yield event
    except Exception as e:
        log_stream_failure(logger, caller, e)
        yield {"event": "error", "data": stream_error_payload(e)}


async def save_assistant_turn(
    *,
    conv_id: uuid.UUID,
    user_id: uuid.UUID,
    content: str,
    metadata: dict,
    profile_notes: list[str] | None = None,
    verdict_kp_id: uuid.UUID | None = None,
    verdict: str | None = None,
    exposed_kp_ids: list[uuid.UUID] | None = None,
    advance_kp_index: int | None = None,
) -> str:
    """Persist a tutor assistant message + post-stream signals in one txn.

    Returns the saved message id. All three tutor endpoints (opening,
    teach, chat answer) funnel through here — differences are expressed
    as kwargs:
      - advance_kp_index: teach turn updates TutorConversation.current_kp_index
      - verdict_*: chat answer may mark a KP understood/needs-clarify
      - exposed_kp_ids: teach turn records exposure on all taught KPs
    """
    from app.models.tutor import TutorConversation, TutorMessage
    from app.services.teaching.signals import apply_post_stream_signals

    async with save_session() as save_db:
        msg = TutorMessage(
            conversation_id=conv_id,
            role="assistant",
            content=content,
            metadata_=metadata,
        )
        save_db.add(msg)

        if advance_kp_index is not None:
            conv = await save_db.get(TutorConversation, conv_id)
            if conv is not None:
                conv.current_kp_index = advance_kp_index

        await apply_post_stream_signals(
            save_db,
            user_id=user_id,
            conv_id=conv_id,
            profile_notes=profile_notes or [],
            verdict_kp_id=verdict_kp_id,
            verdict=verdict,
            exposed_kp_ids=exposed_kp_ids or [],
        )
        await save_db.commit()
        return str(msg.id)
