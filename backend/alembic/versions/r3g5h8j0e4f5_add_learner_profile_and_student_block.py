"""add learner_profile to users and student_block_cache to tutor_conversations

Revision ID: r3g5h8j0e4f5
Revises: q2f4g7i9d2e3
Create Date: 2026-04-18 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "r3g5h8j0e4f5"
down_revision: Union[str, None] = "q2f4g7i9d2e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("learner_profile", sa.Text(), nullable=True),
    )
    op.add_column(
        "tutor_conversations",
        sa.Column("student_block_cache", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("tutor_conversations", "student_block_cache")
    op.drop_column("users", "learner_profile")
