import uuid
from datetime import UTC, datetime
from typing import Literal

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, DateTime, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


TransactionTypeStr = Literal[
    "signup_bonus",
    "subscription_refill",
    "topup_purchase",
    "ai_usage",
    "admin_adjustment",
]


class TransactionType:
    SIGNUP_BONUS: TransactionTypeStr = "signup_bonus"
    SUBSCRIPTION_REFILL: TransactionTypeStr = "subscription_refill"
    TOPUP_PURCHASE: TransactionTypeStr = "topup_purchase"
    AI_USAGE: TransactionTypeStr = "ai_usage"
    ADMIN_ADJUSTMENT: TransactionTypeStr = "admin_adjustment"

    REVENUE: tuple[TransactionTypeStr, ...] = ("subscription_refill", "topup_purchase")


SubscriptionStatusStr = Literal["active", "canceled", "past_due"]


class SubscriptionStatus:
    ACTIVE: SubscriptionStatusStr = "active"
    CANCELED: SubscriptionStatusStr = "canceled"
    PAST_DUE: SubscriptionStatusStr = "past_due"


class SubscriptionPlan(Base):
    """Defines available subscription tiers (seeded data)."""

    __tablename__ = "subscription_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)  # "free", "basic", "pro"
    display_name: Mapped[str] = mapped_column(String(100))  # "Free", "Basic", "Pro"
    monthly_credits: Mapped[int] = mapped_column(Integer)
    price_usd: Mapped[float] = mapped_column(Float)
    stripe_price_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    features: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON blob
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))


class UserSubscription(Base):
    """Tracks a user's current subscription plan."""

    __tablename__ = "user_subscriptions"
    __table_args__ = (UniqueConstraint("user_id", name="uq_user_subscriptions_user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subscription_plans.id"))
    status: Mapped[SubscriptionStatusStr] = mapped_column(String(50), default="active")
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    current_period_start: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))
    current_period_end: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))
    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None), onupdate=lambda: datetime.now(UTC).replace(tzinfo=None))


class CreditBalance(Base):
    """Materialized credit balance per user for fast reads."""

    __tablename__ = "credit_balances"
    __table_args__ = (UniqueConstraint("user_id", name="uq_credit_balances_user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None), onupdate=lambda: datetime.now(UTC).replace(tzinfo=None))


class CreditTransaction(Base):
    """Immutable ledger of all credit changes."""

    __tablename__ = "credit_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    amount: Mapped[int] = mapped_column(Integer)  # positive = grant, negative = deduction
    balance_after: Mapped[int] = mapped_column(Integer)
    transaction_type: Mapped[TransactionTypeStr] = mapped_column(String(50), index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    reference_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None), index=True)
