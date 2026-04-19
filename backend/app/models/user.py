import uuid
from datetime import UTC, date, datetime
from typing import Literal

from sqlalchemy import Boolean, String, Text, Integer, Float, ForeignKey, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


UserRoleStr = Literal["user", "admin"]


class UserRole:
    USER: UserRoleStr = "user"
    ADMIN: UserRoleStr = "admin"


AuthProviderStr = Literal["email", "google"]

# Supported teaching languages. Stored as BCP-47-ish short codes.
SUPPORTED_LANGUAGES: tuple[str, ...] = (
    "en",     # English
    "zh-CN",  # 简体中文
    "ja",     # 日本語
    "ko",     # 한국어
    "es",     # Español
    "fr",     # Français
    "de",     # Deutsch
)
DEFAULT_LANGUAGE = "en"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(500), unique=True)
    name: Mapped[str] = mapped_column(String(500))
    password_hash: Mapped[str | None] = mapped_column(String(500), nullable=True)
    auth_provider: Mapped[AuthProviderStr] = mapped_column(String(50), default="email")
    google_id: Mapped[str | None] = mapped_column(String(500), nullable=True, unique=True)
    avatar_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRoleStr] = mapped_column(String(20), default="user", server_default="user")
    preferred_language: Mapped[str] = mapped_column(
        String(16), default=DEFAULT_LANGUAGE, server_default=DEFAULT_LANGUAGE
    )
    learner_profile: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    knowledge_point_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("knowledge_points.id", ondelete="CASCADE"))
    mastery_level: Mapped[float] = mapped_column(Float, default=0.0)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    interval_days: Mapped[int] = mapped_column(Integer, default=0)
    repetitions: Mapped[int] = mapped_column(Integer, default=0)
    next_review_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_studied_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None), onupdate=lambda: datetime.now(UTC).replace(tzinfo=None))


class UserStreak(Base):
    __tablename__ = "user_streaks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[date] = mapped_column(Date)
    minutes_studied: Mapped[int] = mapped_column(Integer, default=0)
    points_mastered: Mapped[int] = mapped_column(Integer, default=0)
