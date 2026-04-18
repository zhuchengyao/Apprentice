"""drop study_sessions table

The StudySession subsystem has been replaced by TutorConversation / TutorMessage.
Pre-drop data was exported to backend/backups/study_sessions_20260417.sql.

Revision ID: n9c1d4f6a8b9
Revises: m8b0c3e5f7a8
Create Date: 2026-04-17 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "n9c1d4f6a8b9"
down_revision: Union[str, None] = "m8b0c3e5f7a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("study_sessions")


def downgrade() -> None:
    op.create_table(
        "study_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("book_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("books.id", ondelete="CASCADE"), nullable=False),
        sa.Column("section_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sections.id", ondelete="CASCADE"), nullable=False),
        sa.Column("started_at", sa.DateTime, nullable=False),
        sa.Column("ended_at", sa.DateTime, nullable=True),
        sa.Column("interactions", sa.JSON, nullable=True),
        sa.Column("mastery_before", sa.Float, nullable=False, server_default="0.0"),
        sa.Column("mastery_after", sa.Float, nullable=True),
    )
