import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AnimationJobStatus(str, enum.Enum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"
    declined = "declined"


class AnimationJob(Base):
    """Persistent artifact trail for one KP animation generation run.

    The job stores generated pipeline artifacts, not book-derived teaching
    text. In particular, KP explanations are intentionally excluded from
    input_snapshot because they are model-generated downstream text.
    """

    __tablename__ = "animation_jobs"
    __table_args__ = (
        UniqueConstraint("knowledge_point_id", name="uq_animation_jobs_kp"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    knowledge_point_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("knowledge_points.id", ondelete="CASCADE"), index=True
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"), index=True
    )
    chapter_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chapters.id", ondelete="CASCADE"), index=True
    )

    status: Mapped[AnimationJobStatus] = mapped_column(
        SAEnum(AnimationJobStatus), default=AnimationJobStatus.queued, index=True
    )
    concept: Mapped[str] = mapped_column(String(500))
    source_anchor: Mapped[str | None] = mapped_column(Text, nullable=True)
    input_snapshot: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    plan_markdown: Mapped[str | None] = mapped_column(Text, nullable=True)
    scene_spec: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    retrieved_example_ids: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    code_attempts: Mapped[list[dict] | None] = mapped_column(JSONB, nullable=True)
    render_attempts: Mapped[list[dict] | None] = mapped_column(JSONB, nullable=True)
    qc_reports: Mapped[list[dict] | None] = mapped_column(JSONB, nullable=True)

    output_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    failure_kind: Mapped[str | None] = mapped_column(String(50), nullable=True)
    failure_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    decline_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    stage_reached: Mapped[str | None] = mapped_column(String(50), nullable=True)
    attempt: Mapped[int] = mapped_column(Integer, default=0)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    queued_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC).replace(tzinfo=None),
        onupdate=lambda: datetime.now(UTC).replace(tzinfo=None),
    )

    knowledge_point = relationship("KnowledgePoint")
