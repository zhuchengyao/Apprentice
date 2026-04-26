"""add scopes table for parse-stage plan_scopes

Scopes move from a per-session JSONB blob (StudySession.scope_plan) to a
first-class chapter-level artifact. Computed once during chapter parsing
and reused across every learner's session. StudySession.scope_plan stays
(hydrated at session create from the Scope rows) so the session API +
wire shape are unchanged.

Revision ID: w8l0m3o5p7q9
Revises: v7k9l2n4o6p8
Create Date: 2026-04-21 12:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "w8l0m3o5p7q9"
down_revision: Union[str, None] = "v7k9l2n4o6p8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scopes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("chapter_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False),
        sa.Column("index", sa.Integer, nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("anchor_hint", sa.Text, nullable=True),
        sa.Column("kp_ids", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("source_anchors", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("anchors_repaired", sa.Integer, nullable=False, server_default="0"),
        sa.Column("anchors_unmatched", sa.Integer, nullable=False, server_default="0"),
        sa.Column("explanation_text", sa.Text, nullable=True),
        sa.Column("plan_model", sa.String(80), nullable=True),
        sa.Column("plan_hash", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("chapter_id", "index", name="uq_scopes_chapter_index"),
    )
    op.create_index("ix_scopes_chapter_id", "scopes", ["chapter_id"])


def downgrade() -> None:
    op.drop_index("ix_scopes_chapter_id", table_name="scopes")
    op.drop_table("scopes")
