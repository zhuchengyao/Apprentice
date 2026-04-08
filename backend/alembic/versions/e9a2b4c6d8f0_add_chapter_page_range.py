"""add chapter page range and processed flag

Revision ID: e9a2b4c6d8f0
Revises: d8f1a2b3c4e5
Create Date: 2026-04-04 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e9a2b4c6d8f0"
down_revision: Union[str, None] = "d8f1a2b3c4e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("chapters", sa.Column("start_page", sa.Integer(), nullable=False, server_default="1"))
    op.add_column("chapters", sa.Column("end_page", sa.Integer(), nullable=False, server_default="1"))
    op.add_column("chapters", sa.Column("processed", sa.Boolean(), nullable=False, server_default="false"))


def downgrade() -> None:
    op.drop_column("chapters", "processed")
    op.drop_column("chapters", "end_page")
    op.drop_column("chapters", "start_page")
