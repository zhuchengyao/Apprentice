"""Per-request contextvar for the user making AI calls.

user_id threads through many layers (API handler → extractor → AI client →
usage recorder). Carrying it as a function parameter creates param sprawl.
Instead, set it at the entry point (request or background task) and let
_record_usage read it when saving the usage row.
"""

from contextlib import contextmanager
from contextvars import ContextVar

_user_id: ContextVar[str | None] = ContextVar("ai_user_id", default=None)


def get_user_id() -> str | None:
    return _user_id.get()


@contextmanager
def ai_user_context(user_id: str | None):
    token = _user_id.set(user_id)
    try:
        yield
    finally:
        _user_id.reset(token)
