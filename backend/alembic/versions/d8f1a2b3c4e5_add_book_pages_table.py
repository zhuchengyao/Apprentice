"""add book_pages table

Revision ID: d8f1a2b3c4e5
Revises: c7e3a1f90d42
Create Date: 2026-04-04 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d8f1a2b3c4e5"
down_revision: Union[str, None] = "c7e3a1f90d42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "book_pages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "book_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("books.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("page_number", sa.Integer(), nullable=False, index=True),
        sa.Column("html_content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("book_id", "page_number", name="uq_book_pages_book_page"),
    )


def downgrade() -> None:
    op.drop_table("book_pages")
