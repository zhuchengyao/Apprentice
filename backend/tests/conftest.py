"""Shared pytest fixtures for backend tests.

Philosophy: keep the harness light. Rather than spin up Postgres + pgvector
for every test, we override ``get_db`` and ``get_current_user`` at the
FastAPI dependency layer and patch specific service functions per test.
Suites that truly need a real database can opt in with their own fixtures.

Fixtures:
    - ``fake_user``      A fully-constructed ``User`` instance with a stable UUID.
    - ``app``            The FastAPI app with auth + DB dependencies overridden.
    - ``client``         An httpx ``AsyncClient`` wired to the overridden app.
    - ``mock_db``        A ``MagicMock`` standing in for ``AsyncSession``; tests
                         that exercise real DB logic should patch at the
                         call-site (e.g. ``monkeypatch.setattr``) instead.
    - ``mock_llm``       Helper to replace ``iter_llm_chunks`` with a canned
                         async iterator of token strings.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator, Iterable
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.database import get_db
from app.dependencies import get_current_user
from app.main import app as fastapi_app
from app.models.user import User


@pytest.fixture
def fake_user() -> User:
    """A minimal active User. UUID is stable across a test run."""
    return User(
        id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        email="test@example.com",
        name="Test User",
        auth_provider="email",
        is_active=True,
        role="user",
        preferred_language="en",
    )


@pytest.fixture
def mock_db() -> MagicMock:
    """A MagicMock AsyncSession placeholder.

    Most study-API tests should patch the service functions they depend on
    (``_load_session``, ``get_chapter_knowledge_points``, etc.) rather than
    exercising real SQL. This mock is here so dependency-injected handlers
    can receive *something* that looks like an AsyncSession.
    """
    db = MagicMock()
    return db


@pytest.fixture
def app(fake_user: User, mock_db: MagicMock):
    """FastAPI app with auth + DB dependencies swapped for fakes.

    We mutate ``app.dependency_overrides`` rather than re-building the app
    so middleware and route registration match production exactly. The
    finalizer clears overrides so cross-test state never leaks.
    """
    async def _fake_db() -> AsyncIterator[MagicMock]:
        yield mock_db

    async def _fake_user() -> User:
        return fake_user

    fastapi_app.dependency_overrides[get_db] = _fake_db
    fastapi_app.dependency_overrides[get_current_user] = _fake_user
    try:
        yield fastapi_app
    finally:
        fastapi_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture
def mock_llm(monkeypatch: pytest.MonkeyPatch):
    """Replace ``iter_llm_chunks`` with a canned token stream.

    Usage::

        def test_foo(mock_llm):
            mock_llm(["tok1", "tok2"])         # yields two chunks
            mock_llm([])                        # yields nothing (zero-content path)
            mock_llm(RuntimeError("boom"))      # raises mid-stream
    """

    def _install(chunks: Iterable[str] | BaseException):
        async def _fake_iter(**_kwargs):
            if isinstance(chunks, BaseException):
                raise chunks
            for c in chunks:
                yield c

        # Patch at every import site. iter_llm_chunks is re-exported via
        # ``from ... import iter_llm_chunks`` in study.py and tutor.py, so
        # patching only the source module misses those bindings.
        import app.services.teaching.streaming as streaming_mod
        monkeypatch.setattr(streaming_mod, "iter_llm_chunks", _fake_iter)
        for modname in ("app.api.study", "app.api.tutor"):
            try:
                mod = __import__(modname, fromlist=["iter_llm_chunks"])
            except ImportError:
                continue
            if hasattr(mod, "iter_llm_chunks"):
                monkeypatch.setattr(mod, "iter_llm_chunks", _fake_iter)

    return _install
