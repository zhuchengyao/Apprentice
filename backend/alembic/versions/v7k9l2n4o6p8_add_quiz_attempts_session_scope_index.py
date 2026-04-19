"""add composite (session_id, scope_index) index on quiz_attempts

The /answer endpoint and the scope-completion check both filter on
(session_id, scope_index). The single-column ix_quiz_attempts_session_id
forces a heap scan + filter once a session has many attempts; the
composite index lets PostgreSQL satisfy both predicates from the index.

Revision ID: v7k9l2n4o6p8
Revises: u6j8k1m3n5o7
Create Date: 2026-04-19 14:00:00.000000
"""
from typing import Sequence, Union

from alembic import op


revision: str = "v7k9l2n4o6p8"
down_revision: Union[str, None] = "u6j8k1m3n5o7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_quiz_attempts_session_scope",
        "quiz_attempts",
        ["session_id", "scope_index"],
    )


def downgrade() -> None:
    op.drop_index("ix_quiz_attempts_session_scope", table_name="quiz_attempts")
