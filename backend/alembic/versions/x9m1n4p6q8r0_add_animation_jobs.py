"""add persistent animation jobs

Revision ID: x9m1n4p6q8r0
Revises: w8l0m3o5p7q9
Create Date: 2026-04-26 12:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "x9m1n4p6q8r0"
down_revision: Union[str, None] = "w8l0m3o5p7q9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    status_enum = postgresql.ENUM(
        "queued",
        "running",
        "succeeded",
        "failed",
        "declined",
        name="animationjobstatus",
    )
    status_enum.create(op.get_bind(), checkfirst=True)
    status_column_enum = postgresql.ENUM(
        "queued",
        "running",
        "succeeded",
        "failed",
        "declined",
        name="animationjobstatus",
        create_type=False,
    )

    op.create_table(
        "animation_jobs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "knowledge_point_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("knowledge_points.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "book_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("books.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "chapter_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("chapters.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "status",
            status_column_enum,
            nullable=False,
            server_default="queued",
        ),
        sa.Column("concept", sa.String(500), nullable=False),
        sa.Column("source_anchor", sa.Text, nullable=True),
        sa.Column("input_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("plan_markdown", sa.Text, nullable=True),
        sa.Column("scene_spec", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("retrieved_example_ids", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("code_attempts", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("render_attempts", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("qc_reports", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("output_filename", sa.String(255), nullable=True),
        sa.Column("failure_kind", sa.String(50), nullable=True),
        sa.Column("failure_detail", sa.Text, nullable=True),
        sa.Column("decline_reason", sa.Text, nullable=True),
        sa.Column("stage_reached", sa.String(50), nullable=True),
        sa.Column("attempt", sa.Integer, nullable=False, server_default="0"),
        sa.Column("latency_ms", sa.Integer, nullable=True),
        sa.Column("queued_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.Column("started_at", sa.DateTime, nullable=True),
        sa.Column("completed_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("knowledge_point_id", name="uq_animation_jobs_kp"),
    )
    op.create_index("ix_animation_jobs_knowledge_point_id", "animation_jobs", ["knowledge_point_id"])
    op.create_index("ix_animation_jobs_book_id", "animation_jobs", ["book_id"])
    op.create_index("ix_animation_jobs_chapter_id", "animation_jobs", ["chapter_id"])
    op.create_index("ix_animation_jobs_status", "animation_jobs", ["status"])


def downgrade() -> None:
    op.drop_index("ix_animation_jobs_status", table_name="animation_jobs")
    op.drop_index("ix_animation_jobs_chapter_id", table_name="animation_jobs")
    op.drop_index("ix_animation_jobs_book_id", table_name="animation_jobs")
    op.drop_index("ix_animation_jobs_knowledge_point_id", table_name="animation_jobs")
    op.drop_table("animation_jobs")
    postgresql.ENUM(name="animationjobstatus").drop(op.get_bind(), checkfirst=True)
