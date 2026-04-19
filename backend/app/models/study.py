import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, String, Text, Integer, ForeignKey, DateTime, Index, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StudyPhase(str, enum.Enum):
    read = "read"
    explain = "explain"
    practice = "practice"
    feedback = "feedback"
    done = "done"


class StudySession(Base):
    __tablename__ = "study_sessions"
    __table_args__ = (
        UniqueConstraint("user_id", "chapter_id", name="uq_study_sessions_user_chapter"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    chapter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"))
    phase: Mapped[StudyPhase] = mapped_column(SAEnum(StudyPhase), default=StudyPhase.read)
    scope_plan: Mapped[list[dict] | None] = mapped_column(JSONB, nullable=True)
    current_scope_index: Mapped[int] = mapped_column(Integer, default=0)
    current_question_index: Mapped[int] = mapped_column(Integer, default=0)
    tutor_conversation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tutor_conversations.id", ondelete="SET NULL"), nullable=True
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC).replace(tzinfo=None),
        onupdate=lambda: datetime.now(UTC).replace(tzinfo=None),
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    attempts: Mapped[list["QuizAttempt"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", order_by="QuizAttempt.answered_at"
    )


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scope_signature: Mapped[str] = mapped_column(String(64), index=True)
    kp_ids: Mapped[list[str]] = mapped_column(JSONB)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    stem: Mapped[str] = mapped_column(Text)
    options: Mapped[list[dict]] = mapped_column(JSONB)
    correct_option: Mapped[str] = mapped_column(String(1))
    explanation: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(20), default="ai_generated")
    generated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    __table_args__ = (
        Index("ix_quiz_attempts_session_scope", "session_id", "scope_index"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("study_sessions.id", ondelete="CASCADE"), index=True
    )
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quiz_questions.id", ondelete="CASCADE"))
    scope_index: Mapped[int] = mapped_column(Integer)
    chosen_option: Mapped[str] = mapped_column(String(1))
    correct: Mapped[bool] = mapped_column(Boolean, default=False)
    time_spent_ms: Mapped[int] = mapped_column(Integer, default=0)
    answered_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )

    session: Mapped["StudySession"] = relationship(back_populates="attempts")
