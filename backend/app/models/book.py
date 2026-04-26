import enum
import uuid
from datetime import UTC, datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, String, Text, Integer, Float, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BookStatus(str, enum.Enum):
    uploading = "uploading"
    parsing = "parsing"
    extracting = "extracting"
    ready = "ready"
    error = "error"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(500), default="Untitled")
    author: Mapped[str] = mapped_column(String(500), default="Unknown")
    file_path: Mapped[str] = mapped_column(String(1000))
    file_type: Mapped[str] = mapped_column(String(50))
    cover_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    total_pages: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[BookStatus] = mapped_column(SAEnum(BookStatus), default=BookStatus.uploading)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None), onupdate=lambda: datetime.now(UTC).replace(tzinfo=None))

    chapters: Mapped[list["Chapter"]] = relationship(
        back_populates="book", cascade="all, delete-orphan", order_by="Chapter.order_index"
    )
    pages: Mapped[list["BookPage"]] = relationship(
        back_populates="book", cascade="all, delete-orphan", order_by="BookPage.page_number"
    )


class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(500))
    order_index: Mapped[int] = mapped_column(Integer)
    start_page: Mapped[int] = mapped_column(Integer, default=1)
    end_page: Mapped[int] = mapped_column(Integer, default=1)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))

    book: Mapped["Book"] = relationship(back_populates="chapters")
    sections: Mapped[list["Section"]] = relationship(
        back_populates="chapter", cascade="all, delete-orphan", order_by="Section.order_index"
    )


class Section(Base):
    __tablename__ = "sections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(500))
    order_index: Mapped[int] = mapped_column(Integer)
    content_raw: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_markdown: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))

    chapter: Mapped["Chapter"] = relationship(back_populates="sections")
    knowledge_points: Mapped[list["KnowledgePoint"]] = relationship(
        back_populates="section", cascade="all, delete-orphan", order_by="KnowledgePoint.order_index"
    )


class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    section_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"))
    concept: Mapped[str] = mapped_column(String(500))
    explanation: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    order_index: Mapped[int] = mapped_column(Integer)
    image_urls: Mapped[str | None] = mapped_column(Text, nullable=True)
    illustration: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    illustration_video: Mapped[str | None] = mapped_column(String(255), nullable=True)
    question: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_anchor: Mapped[str | None] = mapped_column(Text, nullable=True)
    mastered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))

    section: Mapped["Section"] = relationship(back_populates="knowledge_points")


class BookPage(Base):
    __tablename__ = "book_pages"
    __table_args__ = (
        UniqueConstraint("book_id", "page_number", name="uq_book_pages_book_page"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    page_number: Mapped[int] = mapped_column(Integer, index=True)
    html_content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))

    book: Mapped["Book"] = relationship(back_populates="pages")


class Scope(Base):
    """Parse-stage artifact: an ordered, thematically-grouped unit of study
    within a chapter. Computed once during chapter processing (LLM-driven
    `plan_scopes`) and reused across all sessions, instead of being rebuilt
    per session. `kp_ids` may be a strict subset of the chapter's KPs —
    the LLM is allowed to drop trivia/redundant KPs when planning.

    `source_anchors` are validated + (optionally) repaired at parse time
    against `BookPage.html_content`, so the frontend highlighter hits a
    precise span instead of falling back to a full-container box-shadow.

    `explanation_text` is the pre-warmed scope-level EXPLAIN payload; if
    non-null the frontend can skip the LLM stream on first entry.
    """
    __tablename__ = "scopes"
    __table_args__ = (
        UniqueConstraint("chapter_id", "index", name="uq_scopes_chapter_index"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chapters.id", ondelete="CASCADE"), index=True
    )
    index: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200))
    anchor_hint: Mapped[str | None] = mapped_column(Text, nullable=True)
    kp_ids: Mapped[list[str]] = mapped_column(JSONB)
    source_anchors: Mapped[list[str]] = mapped_column(JSONB)
    anchors_repaired: Mapped[int] = mapped_column(Integer, default=0)
    anchors_unmatched: Mapped[int] = mapped_column(Integer, default=0)
    explanation_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    plan_model: Mapped[str | None] = mapped_column(String(80), nullable=True)
    plan_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )

    chapter: Mapped["Chapter"] = relationship()
