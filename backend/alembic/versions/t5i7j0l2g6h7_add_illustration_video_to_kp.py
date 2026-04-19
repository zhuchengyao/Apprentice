"""add illustration_video to knowledge_points

Stores the MP4 filename produced by the Manim-based animation pipeline.
The legacy `illustration` JSONB column is retained but no longer written.

Revision ID: t5i7j0l2g6h7
Revises: s4h6i9k1f5g6
Create Date: 2026-04-19 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "t5i7j0l2g6h7"
down_revision: Union[str, None] = "s4h6i9k1f5g6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "knowledge_points",
        sa.Column("illustration_video", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("knowledge_points", "illustration_video")
