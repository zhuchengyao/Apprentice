"""add hot-path indexes

Covers queries that run on every tutor turn or chapter open:
  - book_pages filtered by (book_id, page_number BETWEEN ...)
  - tutor_messages loaded via selectinload(conversation_id)
  - sections filtered by chapter_id
  - knowledge_points filtered by section_id
  - user_progress upsert key (user_id, knowledge_point_id)
  - user_progress recent-signals query ordered by last_studied_at

CONCURRENTLY isn't used: this app's tables are small enough that brief
table locks are acceptable and the migration stays simple/reversible.

Revision ID: s4h6i9k1f5g6
Revises: r3g5h8j0e4f5
Create Date: 2026-04-18 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = "s4h6i9k1f5g6"
down_revision: Union[str, None] = "r3g5h8j0e4f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_book_pages_book_page",
        "book_pages",
        ["book_id", "page_number"],
    )
    op.create_index(
        "ix_tutor_messages_conversation_id",
        "tutor_messages",
        ["conversation_id"],
    )
    op.create_index(
        "ix_sections_chapter_id",
        "sections",
        ["chapter_id"],
    )
    op.create_index(
        "ix_knowledge_points_section_id",
        "knowledge_points",
        ["section_id"],
    )
    op.create_index(
        "ix_user_progress_user_kp",
        "user_progress",
        ["user_id", "knowledge_point_id"],
        unique=True,
    )
    op.create_index(
        "ix_user_progress_user_last_studied",
        "user_progress",
        ["user_id", "last_studied_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_user_progress_user_last_studied", table_name="user_progress")
    op.drop_index("ix_user_progress_user_kp", table_name="user_progress")
    op.drop_index("ix_knowledge_points_section_id", table_name="knowledge_points")
    op.drop_index("ix_sections_chapter_id", table_name="sections")
    op.drop_index("ix_tutor_messages_conversation_id", table_name="tutor_messages")
    op.drop_index("ix_book_pages_book_page", table_name="book_pages")
