"""convert knowledge_points.illustration to JSONB

Revision ID: p1e3f6h8c1d2
Revises: o0d2e5g7b0c1
Create Date: 2026-04-17 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "p1e3f6h8c1d2"
down_revision: Union[str, None] = "o0d2e5g7b0c1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # The column is currently TEXT and (as of this migration) always NULL
    # across all environments — no coercion is needed. Any non-null
    # surprises will fail the cast and surface loudly, which is the right
    # behavior: we want to know.
    op.alter_column(
        "knowledge_points",
        "illustration",
        existing_type=sa.Text(),
        type_=postgresql.JSONB(),
        postgresql_using="illustration::jsonb",
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "knowledge_points",
        "illustration",
        existing_type=postgresql.JSONB(),
        type_=sa.Text(),
        postgresql_using="illustration::text",
        existing_nullable=True,
    )
