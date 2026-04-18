"""add source_anchor to knowledge_points

Revision ID: l7a9b2d4e6f7
Revises: k6f8a1c3d5e6
Create Date: 2026-04-15 15:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "l7a9b2d4e6f7"
down_revision: Union[str, None] = "k6f8a1c3d5e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "knowledge_points",
        sa.Column("source_anchor", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("knowledge_points", "source_anchor")
