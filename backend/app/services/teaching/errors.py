"""Structured errors for tutor SSE streams.

Three concerns pushed us to a typed hierarchy over a bare ``except Exception``:

1. Log fidelity — ``logger.error("%s", e)`` drops the stack; every stream
   handler was losing the real traceback, making post-hoc debugging painful.
2. Client safety — SSE handlers were yielding ``str(e)`` directly to the
   browser. A stray ``ValueError`` from the billing layer could leak
   internal identifiers. Clients get a stable shape with no raw internals.
3. Telemetry — classifying errors as LLM vs. persistence vs. credits lets
   us alert differently.
"""

from __future__ import annotations

import json
import logging


class TutorStreamError(Exception):
    """Base for errors raised inside a tutor stream event_stream()."""

    kind: str = "stream_error"
    client_message: str = "An error occurred while streaming the response."


class TutorLLMError(TutorStreamError):
    """The upstream LLM call failed mid-stream."""

    kind = "llm_error"
    client_message = "The tutor is temporarily unavailable. Please try again."


class TutorPersistError(TutorStreamError):
    """Saving the assistant message or applying post-stream signals failed."""

    kind = "persist_error"
    client_message = (
        "The response streamed, but we couldn't save it. "
        "Please retry to keep the conversation in sync."
    )


class CreditsExhausted(TutorStreamError):
    """Credits ran out mid-stream (not a pre-check failure)."""

    kind = "credits_exhausted"
    client_message = "You've run out of credits. Please top up to continue."


def stream_error_payload(exc: BaseException) -> str:
    """Return the JSON-serialized payload for an SSE ``error`` event.

    Shape is stable: ``{"kind": str, "message": str}``. Internal details
    live in logs, never in the stream body.
    """
    if isinstance(exc, TutorStreamError):
        return json.dumps({"kind": exc.kind, "message": exc.client_message})
    return json.dumps(
        {"kind": "stream_error", "message": "Unexpected tutor error."}
    )


def log_stream_failure(
    logger: logging.Logger,
    caller: str,
    exc: BaseException,
) -> None:
    """Emit a structured log for a failed tutor stream. Preserves the stack."""
    kind = exc.kind if isinstance(exc, TutorStreamError) else "stream_error"
    logger.exception(
        "Tutor stream failed",
        extra={"event": "tutor_stream_error", "caller": caller, "kind": kind},
    )
