"""Regression tests for multi-tab phase divergence in the study API.

Covers the server-side guardrails that keep two clients pointed at the
same session from corrupting each other's state:

    1. ``AnswerResponse`` and ``QuestionsResponse`` carry the authoritative
       ``phase`` field so a lagging tab can reconcile without a full resync.
    2. ``POST /study/sessions/{id}/answer`` rejects (409) a question whose
       ``scope_signature`` doesn't match the session's current scope.
"""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.study import QuizQuestion, StudyPhase, StudySession
from app.services.teaching.quiz import scope_signature


KP_CURRENT = [str(uuid.uuid4()), str(uuid.uuid4())]
KP_OTHER = [str(uuid.uuid4())]


def _make_session(fake_user, *, scope_index: int = 0) -> StudySession:
    """A StudySession at scope N with a known kp_ids plan."""
    s = StudySession(
        id=uuid.uuid4(),
        user_id=fake_user.id,
        book_id=uuid.uuid4(),
        chapter_id=uuid.uuid4(),
        phase=StudyPhase.practice,
        scope_plan=[
            {"title": "Scope 0", "kp_ids": KP_CURRENT, "anchor_hint": ""},
            {"title": "Scope 1", "kp_ids": KP_OTHER, "anchor_hint": ""},
        ],
        current_scope_index=scope_index,
        current_question_index=0,
    )
    return s


def _install_session(monkeypatch: pytest.MonkeyPatch, session: StudySession) -> None:
    """Patch study.py's _load_session to return our hand-built session."""
    import app.api.study as study_mod

    async def _fake_load(_id, _user, _db):
        return session

    monkeypatch.setattr(study_mod, "_load_session", _fake_load)


def _install_question(
    mock_db: MagicMock,
    question_id: uuid.UUID,
    question_scope_sig: str,
) -> None:
    """Make ``db.get(QuizQuestion, qid)`` return a question with the given signature."""
    q = QuizQuestion(
        id=question_id,
        scope_signature=question_scope_sig,
        kp_ids=["kp-a"],
        difficulty=1,
        stem="Q",
        options=[{"key": "A", "text": "x"}],
        correct_option="A",
        explanation="",
    )

    async def _get(model, pk):
        if model is QuizQuestion and pk == question_id:
            return q
        return None

    mock_db.get = AsyncMock(side_effect=_get)


@pytest.mark.asyncio
async def test_answer_rejects_cross_scope_question(
    client, fake_user, mock_db, monkeypatch
):
    """A question from the wrong scope must fail with 409, not corrupt state."""
    session = _make_session(fake_user, scope_index=0)
    _install_session(monkeypatch, session)

    qid = uuid.uuid4()
    # Question belongs to a scope whose signature DOES NOT match the
    # session's current scope (scope 0 → KP_CURRENT).
    _install_question(mock_db, qid, scope_signature(["totally-different-kp"]))

    response = await client.post(
        f"/api/study/sessions/{session.id}/answer",
        json={"question_id": str(qid), "chosen_option": "A", "time_spent_ms": 0},
    )

    assert response.status_code == 409
    assert "current scope" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_answer_rejects_when_no_active_scope(
    client, fake_user, mock_db, monkeypatch
):
    """Out-of-range current_scope_index also yields 409, not a 500."""
    session = _make_session(fake_user, scope_index=99)  # past end of plan
    _install_session(monkeypatch, session)

    qid = uuid.uuid4()
    _install_question(mock_db, qid, scope_signature(KP_CURRENT))

    response = await client.post(
        f"/api/study/sessions/{session.id}/answer",
        json={"question_id": str(qid), "chosen_option": "A", "time_spent_ms": 0},
    )

    assert response.status_code == 409
    assert "no active scope" in response.json()["detail"].lower()


def test_response_schemas_include_phase():
    """AnswerResponse + QuestionsResponse must expose a `phase` field.

    This is the contract the frontend relies on for multi-tab reconciliation —
    assert it at the schema layer so it can't silently regress.
    """
    from app.api.study import AnswerResponse, QuestionsResponse

    assert "phase" in AnswerResponse.model_fields
    assert "phase" in QuestionsResponse.model_fields
