"""add study_sessions, quiz_questions, quiz_attempts + study_session_id on tutor_conversations

Introduces the four-phase guided study flow (READ → EXPLAIN → PRACTICE → FEEDBACK).
StudySession persists per-user-per-chapter phase/scope state with a JSONB scope_plan.
QuizQuestion is cached by scope_signature (hash of sorted kp_ids) and reused across users.
QuizAttempt logs every answer for accuracy rollups + adaptive difficulty.

Revision ID: u6j8k1m3n5o7
Revises: t5i7j0l2g6h7
Create Date: 2026-04-19 12:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "u6j8k1m3n5o7"
down_revision: Union[str, None] = "t5i7j0l2g6h7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


STUDY_PHASE = postgresql.ENUM(
    "read", "explain", "practice", "feedback", "done",
    name="studyphase",
    create_type=False,
)


def upgrade() -> None:
    STUDY_PHASE.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "study_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("book_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("books.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chapter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False),
        sa.Column("phase", STUDY_PHASE, nullable=False, server_default="read"),
        sa.Column("scope_plan", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("current_scope_index", sa.Integer, nullable=False, server_default="0"),
        sa.Column("current_question_index", sa.Integer, nullable=False, server_default="0"),
        sa.Column("tutor_conversation_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("started_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("completed_at", sa.DateTime, nullable=True),
        sa.UniqueConstraint("user_id", "chapter_id", name="uq_study_sessions_user_chapter"),
    )

    op.create_table(
        "quiz_questions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scope_signature", sa.String(64), nullable=False),
        sa.Column("kp_ids", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("difficulty", sa.Integer, nullable=False, server_default="1"),
        sa.Column("stem", sa.Text, nullable=False),
        sa.Column("options", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("correct_option", sa.String(1), nullable=False),
        sa.Column("explanation", sa.Text, nullable=False),
        sa.Column("source", sa.String(20), nullable=False, server_default="ai_generated"),
        sa.Column("generated_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_quiz_questions_scope_signature", "quiz_questions", ["scope_signature"])

    op.create_table(
        "quiz_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("study_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("quiz_questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scope_index", sa.Integer, nullable=False),
        sa.Column("chosen_option", sa.String(1), nullable=False),
        sa.Column("correct", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("time_spent_ms", sa.Integer, nullable=False, server_default="0"),
        sa.Column("answered_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_quiz_attempts_session_id", "quiz_attempts", ["session_id"])

    op.create_foreign_key(
        "fk_study_sessions_tutor_conversation_id",
        "study_sessions",
        "tutor_conversations",
        ["tutor_conversation_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.add_column(
        "tutor_conversations",
        sa.Column("study_session_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_tutor_conversations_study_session_id",
        "tutor_conversations",
        "study_sessions",
        ["study_session_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_tutor_conversations_study_session_id", "tutor_conversations", type_="foreignkey")
    op.drop_column("tutor_conversations", "study_session_id")

    op.drop_constraint("fk_study_sessions_tutor_conversation_id", "study_sessions", type_="foreignkey")

    op.drop_index("ix_quiz_attempts_session_id", table_name="quiz_attempts")
    op.drop_table("quiz_attempts")
    op.drop_index("ix_quiz_questions_scope_signature", table_name="quiz_questions")
    op.drop_table("quiz_questions")
    op.drop_table("study_sessions")

    STUDY_PHASE.drop(op.get_bind(), checkfirst=True)
