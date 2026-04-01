"""seed anonymous user

Revision ID: 28052b383f13
Revises: ac6a9449dd23
Create Date: 2026-04-01 16:07:15.089944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28052b383f13'
down_revision: Union[str, None] = 'ac6a9449dd23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "INSERT INTO users (id, email, name, created_at) "
        "VALUES ('00000000-0000-0000-0000-000000000001', "
        "'anonymous@apprentice.local', 'Anonymous', NOW()) "
        "ON CONFLICT (id) DO NOTHING"
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM users WHERE id = '00000000-0000-0000-0000-000000000001'"
    )
