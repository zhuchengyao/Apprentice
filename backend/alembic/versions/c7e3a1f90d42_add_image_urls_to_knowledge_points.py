"""add image_urls to knowledge_points

Revision ID: c7e3a1f90d42
Revises: 42c2b09275b5
Create Date: 2026-04-03 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7e3a1f90d42'
down_revision: Union[str, None] = '42c2b09275b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('knowledge_points', sa.Column('image_urls', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('knowledge_points', 'image_urls')
