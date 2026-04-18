"""cache chapter_context on tutor_conversations

Revision ID: m8b0c3e5f7a8
Revises: l7a9b2d4e6f7
Create Date: 2026-04-17 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "m8b0c3e5f7a8"
down_revision: Union[str, None] = "l7a9b2d4e6f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tutor_conversations",
        sa.Column("chapter_context", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("tutor_conversations", "chapter_context")
