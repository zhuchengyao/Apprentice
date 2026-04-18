"""add auth fields to users and user_id to books

Revision ID: h3c5d7e9f1a3
Revises: g2b4c6d8f1a2
Create Date: 2026-04-09 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "h3c5d7e9f1a3"
down_revision: Union[str, None] = "g2b4c6d8f1a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000001"


def upgrade() -> None:
    # 1. Add auth fields to users
    op.add_column("users", sa.Column("password_hash", sa.String(500), nullable=True))
    op.add_column("users", sa.Column("auth_provider", sa.String(50), nullable=False, server_default="email"))
    op.add_column("users", sa.Column("google_id", sa.String(500), nullable=True))
    op.add_column("users", sa.Column("avatar_url", sa.String(1000), nullable=True))
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"))
    op.create_unique_constraint("uq_users_google_id", "users", ["google_id"])

    # 2. Add user_id to books (nullable first)
    op.add_column("books", sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True))

    # 3. Backfill existing books with default user
    op.execute(f"UPDATE books SET user_id = '{DEFAULT_USER_ID}' WHERE user_id IS NULL")

    # 4. Make user_id NOT NULL and add FK
    op.alter_column("books", "user_id", nullable=False)
    op.create_foreign_key("fk_books_user_id", "books", "users", ["user_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("fk_books_user_id", "books", type_="foreignkey")
    op.drop_column("books", "user_id")
    op.drop_constraint("uq_users_google_id", "users", type_="unique")
    op.drop_column("users", "is_active")
    op.drop_column("users", "avatar_url")
    op.drop_column("users", "google_id")
    op.drop_column("users", "auth_provider")
    op.drop_column("users", "password_hash")
