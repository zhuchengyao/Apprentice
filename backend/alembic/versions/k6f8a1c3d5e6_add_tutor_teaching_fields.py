"""add current_kp_index to tutor_conversations and metadata to tutor_messages

Revision ID: k6f8a1c3d5e6
Revises: j5e7f9b2c3d4
Create Date: 2026-04-12 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "k6f8a1c3d5e6"
down_revision: Union[str, None] = "j5e7f9b2c3d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tutor_conversations",
        sa.Column("current_kp_index", sa.Integer, nullable=False, server_default="0"),
    )
    op.add_column(
        "tutor_messages",
        sa.Column("metadata", sa.JSON, nullable=True),
    )


def downgrade() -> None:
    op.drop_column("tutor_messages", "metadata")
    op.drop_column("tutor_conversations", "current_kp_index")
