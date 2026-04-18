"""Billing API — credits, subscriptions, Stripe checkout & webhooks."""

import json
import logging
import uuid
from datetime import UTC, datetime, timedelta

import stripe
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.billing import (
    CreditBalance,
    CreditTransaction,
    SubscriptionPlan,
    SubscriptionStatus,
    TransactionType,
    UserSubscription,
)
from app.models.usage import ApiUsage
from app.models.user import User
from app.services.billing import add_credits, get_balance, CREDITS_PER_DOLLAR

logger = logging.getLogger(__name__)

router = APIRouter()

stripe.api_key = settings.stripe_secret_key

# ── Credit packs available for purchase ──────────────────────
CREDIT_PACKS = {
    "5000": {"credits": 5000, "price_usd": 5.00, "label": "5,000 credits"},
    "20000": {"credits": 20000, "price_usd": 18.00, "label": "20,000 credits"},
    "50000": {"credits": 50000, "price_usd": 40.00, "label": "50,000 credits"},
}

# ── Pydantic schemas ────────────────────────────────────────


class SubscriptionCheckoutRequest(BaseModel):
    plan_id: str


class CreditCheckoutRequest(BaseModel):
    pack: str  # key from CREDIT_PACKS


# ── Helper ───────────────────────────────────────────────────


async def _get_or_create_stripe_customer(
    db: AsyncSession, user: User, subscription: UserSubscription | None,
) -> str:
    """Get or create Stripe customer, store the ID."""
    if subscription and subscription.stripe_customer_id:
        return subscription.stripe_customer_id

    customer = stripe.Customer.create(
        email=user.email,
        name=user.name,
        metadata={"user_id": str(user.id)},
    )
    if subscription:
        subscription.stripe_customer_id = customer.id
        await db.flush()
    return customer.id


# ── Credits ──────────────────────────────────────────────────


@router.get("/credits")
async def get_credit_balance(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return credit balance and recent transactions."""
    balance = await get_balance(db, current_user.id)

    result = await db.execute(
        select(CreditTransaction)
        .where(CreditTransaction.user_id == current_user.id)
        .order_by(CreditTransaction.created_at.desc())
        .limit(50)
    )
    txns = result.scalars().all()

    return {
        "balance": balance,
        "transactions": [
            {
                "id": str(t.id),
                "amount": t.amount,
                "balance_after": t.balance_after,
                "transaction_type": t.transaction_type,
                "description": t.description,
                "created_at": t.created_at.isoformat(),
            }
            for t in txns
        ],
    }


@router.get("/credits/packs")
async def list_credit_packs():
    """Return available credit packs for purchase."""
    return {"packs": CREDIT_PACKS}


@router.post("/credits/checkout")
async def create_credit_checkout(
    body: CreditCheckoutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a Stripe Checkout session for one-time credit purchase."""
    pack = CREDIT_PACKS.get(body.pack)
    if not pack:
        raise HTTPException(status_code=400, detail=f"Unknown credit pack: {body.pack}")

    if not settings.stripe_secret_key:
        raise HTTPException(status_code=501, detail="Stripe not configured")

    price_cents = int(pack["price_usd"] * 100)

    session = stripe.checkout.Session.create(
        mode="payment",
        customer_email=current_user.email,
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": price_cents,
                "product_data": {"name": pack["label"]},
            },
            "quantity": 1,
        }],
        metadata={
            "user_id": str(current_user.id),
            "type": "credit_topup",
            "credits": str(pack["credits"]),
        },
        success_url=f"{settings.frontend_url}/dashboard?success=credits",
        cancel_url=f"{settings.frontend_url}/dashboard?canceled=credits",
    )

    return {"checkout_url": session.url}


# ── Subscription ─────────────────────────────────────────────


@router.get("/plans")
async def list_plans(db: AsyncSession = Depends(get_db)):
    """Return all active subscription plans."""
    result = await db.execute(
        select(SubscriptionPlan)
        .where(SubscriptionPlan.is_active == True)  # noqa: E712
        .order_by(SubscriptionPlan.price_usd)
    )
    plans = result.scalars().all()
    return {
        "plans": [
            {
                "id": str(p.id),
                "name": p.name,
                "display_name": p.display_name,
                "monthly_credits": p.monthly_credits,
                "price_usd": p.price_usd,
                "stripe_price_id": p.stripe_price_id,
                "features": json.loads(p.features) if p.features else {},
            }
            for p in plans
        ]
    }


@router.get("/subscription")
async def get_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return current user subscription details."""
    result = await db.execute(
        select(UserSubscription)
        .where(UserSubscription.user_id == current_user.id)
    )
    sub = result.scalar_one_or_none()
    if not sub:
        return {"subscription": None}

    plan_result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == sub.plan_id)
    )
    plan = plan_result.scalar_one_or_none()

    return {
        "subscription": {
            "id": str(sub.id),
            "status": sub.status,
            "cancel_at_period_end": sub.cancel_at_period_end,
            "current_period_start": sub.current_period_start.isoformat(),
            "current_period_end": sub.current_period_end.isoformat(),
            "plan": {
                "id": str(plan.id),
                "name": plan.name,
                "display_name": plan.display_name,
                "monthly_credits": plan.monthly_credits,
                "price_usd": plan.price_usd,
                "features": json.loads(plan.features) if plan.features else {},
            } if plan else None,
        }
    }


@router.post("/subscription/checkout")
async def create_subscription_checkout(
    body: SubscriptionCheckoutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create Stripe Checkout session for subscribing to a plan."""
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=501, detail="Stripe not configured")

    plan_result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == uuid.UUID(body.plan_id))
    )
    plan = plan_result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    if not plan.stripe_price_id:
        raise HTTPException(status_code=400, detail="This plan cannot be purchased via Stripe")

    # Get existing subscription
    sub_result = await db.execute(
        select(UserSubscription).where(UserSubscription.user_id == current_user.id)
    )
    sub = sub_result.scalar_one_or_none()

    customer_id = await _get_or_create_stripe_customer(db, current_user, sub)
    await db.commit()

    session = stripe.checkout.Session.create(
        mode="subscription",
        customer=customer_id,
        line_items=[{"price": plan.stripe_price_id, "quantity": 1}],
        metadata={
            "user_id": str(current_user.id),
            "type": "subscription",
            "plan_id": str(plan.id),
        },
        success_url=f"{settings.frontend_url}/dashboard?success=subscription",
        cancel_url=f"{settings.frontend_url}/dashboard?canceled=subscription",
    )

    return {"checkout_url": session.url}


@router.post("/subscription/portal")
async def create_billing_portal(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create Stripe Billing Portal session for managing subscription."""
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=501, detail="Stripe not configured")

    sub_result = await db.execute(
        select(UserSubscription).where(UserSubscription.user_id == current_user.id)
    )
    sub = sub_result.scalar_one_or_none()
    if not sub or not sub.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No Stripe subscription found")

    session = stripe.billing_portal.Session.create(
        customer=sub.stripe_customer_id,
        return_url=f"{settings.frontend_url}/dashboard",
    )

    return {"portal_url": session.url}


@router.post("/subscription/cancel")
async def cancel_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark subscription to cancel at period end."""
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=501, detail="Stripe not configured")

    sub_result = await db.execute(
        select(UserSubscription).where(UserSubscription.user_id == current_user.id)
    )
    sub = sub_result.scalar_one_or_none()
    if not sub or not sub.stripe_subscription_id:
        raise HTTPException(status_code=400, detail="No active subscription to cancel")

    stripe.Subscription.modify(
        sub.stripe_subscription_id,
        cancel_at_period_end=True,
    )

    sub.cancel_at_period_end = True
    await db.commit()

    return {"status": "canceling", "cancel_at_period_end": True}


# ── Usage ────────────────────────────────────────────────────


@router.get("/usage")
async def get_user_usage(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Per-user usage summary: total credits used, breakdown by caller, daily data."""
    since = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=days)

    # Breakdown by caller
    result = await db.execute(
        select(
            ApiUsage.caller,
            func.count(ApiUsage.id).label("calls"),
            func.sum(ApiUsage.input_tokens).label("input_tokens"),
            func.sum(ApiUsage.output_tokens).label("output_tokens"),
            func.sum(ApiUsage.cost_usd).label("cost_usd"),
        )
        .where(ApiUsage.user_id == current_user.id, ApiUsage.created_at >= since)
        .group_by(ApiUsage.caller)
        .order_by(func.sum(ApiUsage.cost_usd).desc())
    )
    rows = result.all()

    total_cost = 0.0
    total_calls = 0
    breakdown = []
    for row in rows:
        cost = float(row.cost_usd or 0)
        calls = int(row.calls or 0)
        total_cost += cost
        total_calls += calls
        breakdown.append({
            "caller": row.caller,
            "calls": calls,
            "input_tokens": int(row.input_tokens or 0),
            "output_tokens": int(row.output_tokens or 0),
            "cost_usd": round(cost, 6),
            "credits_used": int(cost * CREDITS_PER_DOLLAR),
        })

    # Daily aggregation for chart
    daily_result = await db.execute(
        select(
            func.date_trunc("day", ApiUsage.created_at).label("day"),
            func.sum(ApiUsage.cost_usd).label("cost_usd"),
            func.count(ApiUsage.id).label("calls"),
        )
        .where(ApiUsage.user_id == current_user.id, ApiUsage.created_at >= since)
        .group_by(func.date_trunc("day", ApiUsage.created_at))
        .order_by(func.date_trunc("day", ApiUsage.created_at))
    )
    daily_rows = daily_result.all()

    daily = [
        {
            "date": row.day.strftime("%Y-%m-%d"),
            "cost_usd": round(float(row.cost_usd or 0), 6),
            "credits_used": int(float(row.cost_usd or 0) * CREDITS_PER_DOLLAR),
            "calls": int(row.calls or 0),
        }
        for row in daily_rows
    ]

    return {
        "period_days": days,
        "total_calls": total_calls,
        "total_cost_usd": round(total_cost, 6),
        "total_credits_used": int(total_cost * CREDITS_PER_DOLLAR),
        "breakdown": breakdown,
        "daily": daily,
    }


# ── Stripe Webhook ───────────────────────────────────────────


@router.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle Stripe webhook events. No JWT auth — uses Stripe signature."""
    if not settings.stripe_webhook_secret:
        raise HTTPException(status_code=501, detail="Webhook secret not configured")

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret,
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    event_type = event["type"]
    data = event["data"]["object"]

    logger.info("Stripe webhook: %s", event_type)

    if event_type == "checkout.session.completed":
        await _handle_checkout_completed(db, data)
    elif event_type == "invoice.paid":
        await _handle_invoice_paid(db, data)
    elif event_type == "customer.subscription.updated":
        await _handle_subscription_updated(db, data)
    elif event_type == "customer.subscription.deleted":
        await _handle_subscription_deleted(db, data)

    await db.commit()
    return {"status": "ok"}


async def _handle_checkout_completed(db: AsyncSession, session: dict):
    """Handle completed checkout — credit top-up or subscription."""
    metadata = session.get("metadata", {})
    user_id_str = metadata.get("user_id")
    checkout_type = metadata.get("type")

    if not user_id_str:
        logger.warning("Checkout completed without user_id in metadata")
        return

    user_id = uuid.UUID(user_id_str)

    if checkout_type == "credit_topup":
        credits = int(metadata.get("credits", 0))
        if credits > 0:
            await add_credits(
                db, user_id, credits,
                transaction_type=TransactionType.TOPUP_PURCHASE,
                description=f"Credit purchase ({credits} credits)",
            )
            logger.info("Added %d credits to user %s", credits, user_id)

    elif checkout_type == "subscription":
        plan_id = metadata.get("plan_id")
        stripe_sub_id = session.get("subscription")
        stripe_customer_id = session.get("customer")

        if plan_id and stripe_sub_id:
            sub_result = await db.execute(
                select(UserSubscription).where(UserSubscription.user_id == user_id)
            )
            sub = sub_result.scalar_one_or_none()
            if sub:
                sub.plan_id = uuid.UUID(plan_id)
                sub.status = SubscriptionStatus.ACTIVE
                sub.stripe_subscription_id = stripe_sub_id
                sub.stripe_customer_id = stripe_customer_id
                sub.current_period_start = datetime.now(UTC).replace(tzinfo=None)
                sub.current_period_end = datetime.now(UTC).replace(tzinfo=None) + timedelta(days=30)
                sub.cancel_at_period_end = False

                # Grant initial monthly credits
                plan_result = await db.execute(
                    select(SubscriptionPlan).where(SubscriptionPlan.id == uuid.UUID(plan_id))
                )
                plan = plan_result.scalar_one_or_none()
                if plan:
                    await add_credits(
                        db, user_id, plan.monthly_credits,
                        transaction_type=TransactionType.SUBSCRIPTION_REFILL,
                        description=f"Subscription to {plan.display_name}",
                    )
            logger.info("Subscription created for user %s, plan %s", user_id, plan_id)


async def _handle_invoice_paid(db: AsyncSession, invoice: dict):
    """Handle subscription renewal — refill credits."""
    stripe_sub_id = invoice.get("subscription")
    if not stripe_sub_id:
        return

    sub_result = await db.execute(
        select(UserSubscription).where(UserSubscription.stripe_subscription_id == stripe_sub_id)
    )
    sub = sub_result.scalar_one_or_none()
    if not sub:
        return

    # Skip if this is the first invoice (handled by checkout.session.completed)
    billing_reason = invoice.get("billing_reason")
    if billing_reason == "subscription_create":
        return

    plan_result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == sub.plan_id)
    )
    plan = plan_result.scalar_one_or_none()
    if not plan:
        return

    # Update period
    sub.current_period_start = datetime.now(UTC).replace(tzinfo=None)
    sub.current_period_end = datetime.now(UTC).replace(tzinfo=None) + timedelta(days=30)
    sub.status = SubscriptionStatus.ACTIVE

    await add_credits(
        db, sub.user_id, plan.monthly_credits,
        transaction_type=TransactionType.SUBSCRIPTION_REFILL,
        description=f"Monthly refill ({plan.display_name})",
    )
    logger.info("Refilled %d credits for user %s", plan.monthly_credits, sub.user_id)


async def _handle_subscription_updated(db: AsyncSession, subscription: dict):
    """Handle subscription plan change or status update."""
    stripe_sub_id = subscription.get("id")
    sub_result = await db.execute(
        select(UserSubscription).where(UserSubscription.stripe_subscription_id == stripe_sub_id)
    )
    sub = sub_result.scalar_one_or_none()
    if not sub:
        return

    sub.status = subscription.get("status", sub.status)
    sub.cancel_at_period_end = subscription.get("cancel_at_period_end", False)


async def _handle_subscription_deleted(db: AsyncSession, subscription: dict):
    """Handle subscription cancellation — downgrade to free."""
    stripe_sub_id = subscription.get("id")
    sub_result = await db.execute(
        select(UserSubscription).where(UserSubscription.stripe_subscription_id == stripe_sub_id)
    )
    sub = sub_result.scalar_one_or_none()
    if not sub:
        return

    # Find free plan
    free_result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.name == "free")
    )
    free_plan = free_result.scalar_one_or_none()

    if free_plan:
        sub.plan_id = free_plan.id
    sub.status = SubscriptionStatus.CANCELED
    sub.stripe_subscription_id = None
    sub.cancel_at_period_end = False

    logger.info("User %s downgraded to free plan", sub.user_id)
