"""Credit system core: balance management, deduction, enforcement."""

import logging
import math
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.billing import (
    CreditBalance,
    CreditTransaction,
    SubscriptionPlan,
    SubscriptionStatus,
    TransactionType,
    UserSubscription,
)
from app.services.ai_client import MODEL_PRICING

logger = logging.getLogger(__name__)

CREDITS_PER_DOLLAR = 1000  # 1 credit = $0.001 USD

# Stable UUID for the free plan (must match migration seed)
FREE_PLAN_ID = uuid.UUID("00000000-0000-0000-0000-000000000101")
SIGNUP_BONUS_CREDITS = 500


def cost_to_credits(cost_usd: float) -> int:
    """Convert a USD cost to credits. Always rounds up so no free usage."""
    return max(1, math.ceil(cost_usd * CREDITS_PER_DOLLAR))


def estimate_max_credits(model: str, max_tokens: int, estimated_input_tokens: int = 2000) -> int:
    """Conservative upper-bound credit cost for an AI call."""
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        return 50
    max_cost = (estimated_input_tokens * pricing["input"] + max_tokens * pricing["output"]) / 1_000_000
    return cost_to_credits(max_cost)


async def get_balance(db: AsyncSession, user_id: uuid.UUID) -> int:
    """Read current credit balance for a user."""
    result = await db.execute(
        select(CreditBalance.balance).where(CreditBalance.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    return row if row is not None else 0


async def add_credits(
    db: AsyncSession,
    user_id: uuid.UUID,
    amount: int,
    transaction_type: str,
    description: str | None = None,
    reference_id: uuid.UUID | None = None,
) -> int:
    """Atomically add credits and record a ledger entry. Returns new balance."""
    # Lock the balance row
    result = await db.execute(
        select(CreditBalance)
        .where(CreditBalance.user_id == user_id)
        .with_for_update()
    )
    balance_row = result.scalar_one_or_none()

    if not balance_row:
        balance_row = CreditBalance(user_id=user_id, balance=0)
        db.add(balance_row)
        await db.flush()
        # Re-select with lock
        result = await db.execute(
            select(CreditBalance)
            .where(CreditBalance.user_id == user_id)
            .with_for_update()
        )
        balance_row = result.scalar_one()

    balance_row.balance += amount
    new_balance = balance_row.balance

    db.add(CreditTransaction(
        user_id=user_id,
        amount=amount,
        balance_after=new_balance,
        transaction_type=transaction_type,
        description=description,
        reference_id=reference_id,
    ))

    return new_balance


async def deduct_credits_for_usage(
    db: AsyncSession,
    user_id: str,
    usage_id: uuid.UUID,
    cost_usd: float,
) -> None:
    """Deduct credits for an AI usage record. Called inside _record_usage transaction."""
    credits = cost_to_credits(cost_usd)
    uid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    await add_credits(
        db=db,
        user_id=uid,
        amount=-credits,
        transaction_type=TransactionType.AI_USAGE,
        description=f"AI call (${cost_usd:.6f})",
        reference_id=usage_id,
    )


async def check_credits_or_raise(
    db: AsyncSession,
    user_id: uuid.UUID,
    model: str,
    max_tokens: int,
    estimated_input_tokens: int = 2000,
) -> None:
    """Raise HTTP 402 if user lacks credits for an estimated AI call."""
    needed = estimate_max_credits(model, max_tokens, estimated_input_tokens)
    balance = await get_balance(db, user_id)
    if balance < needed:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "insufficient_credits",
                "balance": balance,
                "estimated_cost": needed,
                "message": "Insufficient credits. Please purchase more credits or upgrade your plan.",
            },
        )


async def ensure_user_billing(db: AsyncSession, user_id: uuid.UUID) -> None:
    """Create CreditBalance + UserSubscription (free plan) for a new user, with signup bonus."""
    # Check if already exists
    existing = await db.execute(
        select(CreditBalance).where(CreditBalance.user_id == user_id)
    )
    if existing.scalar_one_or_none():
        return

    # Create balance with signup bonus
    balance_row = CreditBalance(user_id=user_id, balance=SIGNUP_BONUS_CREDITS)
    db.add(balance_row)

    # Record signup bonus transaction
    db.add(CreditTransaction(
        user_id=user_id,
        amount=SIGNUP_BONUS_CREDITS,
        balance_after=SIGNUP_BONUS_CREDITS,
        transaction_type=TransactionType.SIGNUP_BONUS,
        description="Welcome bonus credits",
    ))

    # Create free subscription
    db.add(UserSubscription(
        user_id=user_id,
        plan_id=FREE_PLAN_ID,
        status=SubscriptionStatus.ACTIVE,
    ))

    await db.flush()
