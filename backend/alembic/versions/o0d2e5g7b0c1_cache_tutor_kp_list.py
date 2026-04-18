"""cache tutor kp_list

Revision ID: o0d2e5g7b0c1
Revises: n9c1d4f6a8b9
Create Date: 2026-04-17 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "o0d2e5g7b0c1"
down_revision: Union[str, None] = "n9c1d4f6a8b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tutor_conversations",
        sa.Column("kp_list_cache", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("tutor_conversations", "kp_list_cache")
