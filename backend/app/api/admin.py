"""Admin API — site-wide monitoring and user management.

All routes require role='admin'. Every write action is logged to
admin_audit_logs. Reads are free but still admin-gated.
"""

import json
import logging
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import execute_parallel, get_db
from app.dependencies import get_current_admin
from app.models.admin import AdminAuditLog
from app.models.billing import (
    CreditBalance,
    CreditTransaction,
    SubscriptionPlan,
    SubscriptionStatus,
    TransactionType,
    UserSubscription,
)
from app.models.book import Book, BookStatus
from app.models.tutor import TutorConversation, TutorMessage
from app.models.usage import ApiUsage
from app.models.user import User
from app.services.admin import log_admin_action
from app.services.billing import CREDITS_PER_DOLLAR, add_credits, get_balance

logger = logging.getLogger(__name__)

router = APIRouter()


# ── Schemas ──────────────────────────────────────────────────


class AdjustCreditsRequest(BaseModel):
    amount: int = Field(..., description="Positive to grant, negative to deduct")
    reason: str = Field(..., min_length=3, max_length=500)


class ToggleActiveRequest(BaseModel):
    is_active: bool
    reason: str = Field(..., min_length=3, max_length=500)


class SetRoleRequest(BaseModel):
    role: str = Field(..., pattern="^(user|admin)$")
    reason: str = Field(..., min_length=3, max_length=500)


# ── Identity ─────────────────────────────────────────────────


@router.get("/me")
async def admin_me(admin: User = Depends(get_current_admin)):
    """Verify admin session. Returns basic profile if caller is admin, else 403."""
    return {
        "id": str(admin.id),
        "email": admin.email,
        "name": admin.name,
        "role": admin.role,
    }


# ── Overview: site-wide stats ────────────────────────────────


@router.get("/overview")
async def admin_overview(
    days: int = Query(30, ge=1, le=365),
    _admin: User = Depends(get_current_admin),
):
    """Global monitoring dashboard: users, revenue, AI cost, activity."""
    now = datetime.now(UTC).replace(tzinfo=None)
    since = now - timedelta(days=days)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Revenue = subscription refills + topup purchases. Credits granted / CREDITS_PER_DOLLAR = USD.
    revenue_where = (
        CreditTransaction.transaction_type.in_(TransactionType.REVENUE),
        CreditTransaction.created_at >= since,
    )
    usage_since = ApiUsage.created_at >= since

    stmts = [
        # users
        select(
            func.count(User.id).label("total"),
            func.count(User.id).filter(User.is_active == True).label("active"),  # noqa: E712
            func.count(User.id).filter(User.created_at >= today_start).label("new_today"),
            func.count(User.id).filter(User.created_at >= since).label("new_period"),
        ),
        # active users in period (distinct callers of AI)
        select(func.count(func.distinct(ApiUsage.user_id)))
        .where(usage_since, ApiUsage.user_id.isnot(None)),
        # books
        select(
            func.count(Book.id).label("total"),
            func.count(Book.id).filter(Book.status == BookStatus.ready).label("ready"),
            func.count(Book.id).filter(Book.status == BookStatus.error).label("failed"),
        ),
        # revenue total
        select(func.coalesce(func.sum(CreditTransaction.amount), 0).label("credits"))
        .where(*revenue_where),
        # revenue by type
        select(
            CreditTransaction.transaction_type,
            func.coalesce(func.sum(CreditTransaction.amount), 0).label("credits"),
        ).where(*revenue_where).group_by(CreditTransaction.transaction_type),
        # AI cost totals
        select(
            func.coalesce(func.sum(ApiUsage.cost_usd), 0).label("cost"),
            func.count(ApiUsage.id).label("calls"),
            func.coalesce(func.sum(ApiUsage.input_tokens), 0).label("input_tokens"),
            func.coalesce(func.sum(ApiUsage.output_tokens), 0).label("output_tokens"),
        ).where(usage_since),
        # cost by caller
        select(
            ApiUsage.caller,
            func.count(ApiUsage.id).label("calls"),
            func.coalesce(func.sum(ApiUsage.cost_usd), 0).label("cost"),
        ).where(usage_since).group_by(ApiUsage.caller).order_by(desc("cost")),
        # cost by model
        select(
            ApiUsage.model,
            func.count(ApiUsage.id).label("calls"),
            func.coalesce(func.sum(ApiUsage.cost_usd), 0).label("cost"),
        ).where(usage_since).group_by(ApiUsage.model).order_by(desc("cost")),
        # daily cost
        select(
            func.date_trunc("day", ApiUsage.created_at).label("day"),
            func.coalesce(func.sum(ApiUsage.cost_usd), 0).label("cost"),
        ).where(usage_since).group_by("day").order_by("day"),
        # daily revenue
        select(
            func.date_trunc("day", CreditTransaction.created_at).label("day"),
            func.coalesce(func.sum(CreditTransaction.amount), 0).label("credits"),
        ).where(*revenue_where).group_by("day").order_by("day"),
        # top consumers
        select(
            ApiUsage.user_id,
            User.email,
            User.name,
            func.count(ApiUsage.id).label("calls"),
            func.coalesce(func.sum(ApiUsage.cost_usd), 0).label("cost"),
        )
        .join(User, User.id == ApiUsage.user_id)
        .where(usage_since, ApiUsage.user_id.isnot(None))
        .group_by(ApiUsage.user_id, User.email, User.name)
        .order_by(desc("cost"))
        .limit(10),
        # subscription distribution
        select(
            SubscriptionPlan.name,
            SubscriptionPlan.display_name,
            func.count(UserSubscription.id).label("count"),
        )
        .join(UserSubscription, UserSubscription.plan_id == SubscriptionPlan.id)
        .where(UserSubscription.status == SubscriptionStatus.ACTIVE)
        .group_by(SubscriptionPlan.name, SubscriptionPlan.display_name),
        # tutor totals
        select(func.count(TutorConversation.id)),
        # tutor messages in period
        select(func.count(TutorMessage.id)).where(TutorMessage.created_at >= since),
    ]

    (
        user_result, active_result, book_result, revenue_result,
        revenue_by_type_result, cost_result, cost_by_caller_result,
        cost_by_model_result, day_cost_result, day_rev_result,
        top_consumers_result, sub_dist_result, tutor_result, msg_result,
    ) = await execute_parallel(*stmts)

    u = user_result.one()
    active_period = int(active_result.scalar() or 0)
    b = book_result.one()
    revenue_usd = int(revenue_result.scalar() or 0) / CREDITS_PER_DOLLAR
    revenue_by_type = {
        row.transaction_type: round(int(row.credits or 0) / CREDITS_PER_DOLLAR, 2)
        for row in revenue_by_type_result.all()
    }
    c = cost_result.one()
    total_cost_usd = float(c.cost or 0)
    cost_by_caller = [
        {
            "caller": row.caller,
            "calls": int(row.calls or 0),
            "cost_usd": round(float(row.cost or 0), 6),
        }
        for row in cost_by_caller_result.all()
    ]
    cost_by_model = [
        {
            "model": row.model,
            "calls": int(row.calls or 0),
            "cost_usd": round(float(row.cost or 0), 6),
        }
        for row in cost_by_model_result.all()
    ]
    daily_cost_map = {
        row.day.strftime("%Y-%m-%d"): round(float(row.cost or 0), 6)
        for row in day_cost_result.all()
    }
    daily_rev_map = {
        row.day.strftime("%Y-%m-%d"): round(int(row.credits or 0) / CREDITS_PER_DOLLAR, 2)
        for row in day_rev_result.all()
    }
    daily = [
        {
            "date": d,
            "cost_usd": daily_cost_map.get(d, 0.0),
            "revenue_usd": daily_rev_map.get(d, 0.0),
        }
        for d in sorted(set(daily_cost_map.keys()) | set(daily_rev_map.keys()))
    ]
    top_consumers = [
        {
            "user_id": str(row.user_id),
            "email": row.email,
            "name": row.name,
            "calls": int(row.calls or 0),
            "cost_usd": round(float(row.cost or 0), 6),
        }
        for row in top_consumers_result.all()
    ]
    subscriptions = [
        {
            "plan_name": row.name,
            "display_name": row.display_name,
            "count": int(row.count or 0),
        }
        for row in sub_dist_result.all()
    ]
    total_conv = int(tutor_result.scalar() or 0)
    period_msgs = int(msg_result.scalar() or 0)

    return {
        "period_days": days,
        "users": {
            "total": int(u.total or 0),
            "active": int(u.active or 0),
            "new_today": int(u.new_today or 0),
            "new_in_period": int(u.new_period or 0),
            "active_in_period": active_period,
        },
        "books": {
            "total": int(b.total or 0),
            "ready": int(b.ready or 0),
            "failed": int(b.failed or 0),
        },
        "revenue": {
            "total_usd": round(revenue_usd, 2),
            "by_type": revenue_by_type,
        },
        "cost": {
            "total_usd": round(total_cost_usd, 6),
            "total_calls": int(c.calls or 0),
            "input_tokens": int(c.input_tokens or 0),
            "output_tokens": int(c.output_tokens or 0),
            "by_caller": cost_by_caller,
            "by_model": cost_by_model,
        },
        "profit": {
            "total_usd": round(revenue_usd - total_cost_usd, 2),
        },
        "daily": daily,
        "top_consumers": top_consumers,
        "subscriptions": subscriptions,
        "tutor": {
            "total_conversations": total_conv,
            "messages_in_period": period_msgs,
        },
    }


# ── Users ────────────────────────────────────────────────────


@router.get("/users")
async def list_users(
    q: str | None = Query(None, description="Email or name substring"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Paginated user list with optional search."""
    base_filters = []
    if q:
        like = f"%{q}%"
        base_filters.append(or_(User.email.ilike(like), User.name.ilike(like)))

    count_stmt = select(func.count(User.id))
    if base_filters:
        count_stmt = count_stmt.where(and_(*base_filters))
    total = int((await db.execute(count_stmt)).scalar() or 0)

    stmt = (
        select(
            User.id,
            User.email,
            User.name,
            User.role,
            User.is_active,
            User.auth_provider,
            User.created_at,
            CreditBalance.balance,
            SubscriptionPlan.name.label("plan_name"),
            SubscriptionPlan.display_name.label("plan_display"),
        )
        .outerjoin(CreditBalance, CreditBalance.user_id == User.id)
        .outerjoin(UserSubscription, UserSubscription.user_id == User.id)
        .outerjoin(SubscriptionPlan, SubscriptionPlan.id == UserSubscription.plan_id)
        .order_by(User.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    if base_filters:
        stmt = stmt.where(and_(*base_filters))

    rows = (await db.execute(stmt)).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "users": [
            {
                "id": str(row.id),
                "email": row.email,
                "name": row.name,
                "role": row.role,
                "is_active": row.is_active,
                "auth_provider": row.auth_provider,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "balance": int(row.balance or 0),
                "plan": {
                    "name": row.plan_name,
                    "display_name": row.plan_display,
                } if row.plan_name else None,
            }
            for row in rows
        ],
    }


@router.get("/users/{user_id}")
async def get_user_detail(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Full profile: user + balance + subscription + recent txns + book count."""
    uid = uuid.UUID(user_id)
    user = await db.get(User, uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    balance = await get_balance(db, uid)

    sub_result = await db.execute(
        select(UserSubscription, SubscriptionPlan)
        .join(SubscriptionPlan, SubscriptionPlan.id == UserSubscription.plan_id)
        .where(UserSubscription.user_id == uid)
    )
    sub_row = sub_result.one_or_none()

    txn_result = await db.execute(
        select(CreditTransaction)
        .where(CreditTransaction.user_id == uid)
        .order_by(CreditTransaction.created_at.desc())
        .limit(20)
    )
    txns = txn_result.scalars().all()

    book_count_result = await db.execute(
        select(func.count(Book.id)).where(Book.user_id == uid)
    )
    book_count = int(book_count_result.scalar() or 0)

    conv_count_result = await db.execute(
        select(func.count(TutorConversation.id)).where(TutorConversation.user_id == uid)
    )
    conv_count = int(conv_count_result.scalar() or 0)

    usage_result = await db.execute(
        select(
            func.coalesce(func.sum(ApiUsage.cost_usd), 0).label("cost"),
            func.count(ApiUsage.id).label("calls"),
        )
        .where(ApiUsage.user_id == uid)
    )
    usage_row = usage_result.one()

    return {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "is_active": user.is_active,
            "auth_provider": user.auth_provider,
            "avatar_url": user.avatar_url,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        },
        "balance": balance,
        "subscription": (
            {
                "id": str(sub_row.UserSubscription.id),
                "status": sub_row.UserSubscription.status,
                "current_period_end": sub_row.UserSubscription.current_period_end.isoformat(),
                "cancel_at_period_end": sub_row.UserSubscription.cancel_at_period_end,
                "plan": {
                    "name": sub_row.SubscriptionPlan.name,
                    "display_name": sub_row.SubscriptionPlan.display_name,
                    "monthly_credits": sub_row.SubscriptionPlan.monthly_credits,
                    "price_usd": sub_row.SubscriptionPlan.price_usd,
                },
            }
            if sub_row
            else None
        ),
        "stats": {
            "book_count": book_count,
            "conversation_count": conv_count,
            "lifetime_ai_calls": int(usage_row.calls or 0),
            "lifetime_cost_usd": round(float(usage_row.cost or 0), 6),
        },
        "recent_transactions": [
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


@router.patch("/users/{user_id}/active")
async def toggle_user_active(
    user_id: str,
    body: ToggleActiveRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Enable or disable a user account."""
    uid = uuid.UUID(user_id)
    user = await db.get(User, uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot disable your own account")

    previous = user.is_active
    user.is_active = body.is_active

    await log_admin_action(
        db,
        actor_id=admin.id,
        action="user.toggle_active",
        target_user_id=uid,
        details={"previous": previous, "new": body.is_active},
        reason=body.reason,
    )

    await db.commit()
    return {"id": str(user.id), "is_active": user.is_active}


@router.post("/users/{user_id}/credits")
async def adjust_user_credits(
    user_id: str,
    body: AdjustCreditsRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Grant or deduct credits for a user. Writes both a CreditTransaction
    and an AdminAuditLog entry in a single transaction."""
    uid = uuid.UUID(user_id)
    user = await db.get(User, uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if body.amount == 0:
        raise HTTPException(status_code=400, detail="Amount must be non-zero")

    new_balance = await add_credits(
        db,
        user_id=uid,
        amount=body.amount,
        transaction_type=TransactionType.ADMIN_ADJUSTMENT,
        description=f"Admin adjustment: {body.reason}",
    )

    await log_admin_action(
        db,
        actor_id=admin.id,
        action="user.credit_adjustment",
        target_user_id=uid,
        details={"amount": body.amount, "new_balance": new_balance},
        reason=body.reason,
    )

    await db.commit()
    return {"user_id": str(uid), "amount": body.amount, "new_balance": new_balance}


@router.patch("/users/{user_id}/role")
async def set_user_role(
    user_id: str,
    body: SetRoleRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Promote or demote a user's role."""
    uid = uuid.UUID(user_id)
    user = await db.get(User, uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id and body.role != "admin":
        raise HTTPException(status_code=400, detail="Cannot demote yourself")

    previous = user.role
    user.role = body.role

    await log_admin_action(
        db,
        actor_id=admin.id,
        action="user.set_role",
        target_user_id=uid,
        details={"previous": previous, "new": body.role},
        reason=body.reason,
    )

    await db.commit()
    return {"id": str(user.id), "role": user.role}


# ── Audit log ────────────────────────────────────────────────


@router.get("/audit")
async def list_audit_logs(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    action: str | None = None,
    actor_id: str | None = None,
    target_user_id: str | None = None,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Return recent admin actions with filters."""
    filters = []
    if action:
        filters.append(AdminAuditLog.action == action)
    if actor_id:
        filters.append(AdminAuditLog.actor_id == uuid.UUID(actor_id))
    if target_user_id:
        filters.append(AdminAuditLog.target_user_id == uuid.UUID(target_user_id))

    count_stmt = select(func.count(AdminAuditLog.id))
    if filters:
        count_stmt = count_stmt.where(and_(*filters))
    total = int((await db.execute(count_stmt)).scalar() or 0)

    actor_alias = User.__table__.alias("actor")
    target_alias = User.__table__.alias("target")

    stmt = (
        select(
            AdminAuditLog.id,
            AdminAuditLog.action,
            AdminAuditLog.details,
            AdminAuditLog.reason,
            AdminAuditLog.created_at,
            AdminAuditLog.actor_id,
            AdminAuditLog.target_user_id,
            actor_alias.c.email.label("actor_email"),
            target_alias.c.email.label("target_email"),
        )
        .outerjoin(actor_alias, actor_alias.c.id == AdminAuditLog.actor_id)
        .outerjoin(target_alias, target_alias.c.id == AdminAuditLog.target_user_id)
        .order_by(AdminAuditLog.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    if filters:
        stmt = stmt.where(and_(*filters))

    rows = (await db.execute(stmt)).all()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "logs": [
            {
                "id": str(row.id),
                "action": row.action,
                "actor": {
                    "id": str(row.actor_id),
                    "email": row.actor_email,
                },
                "target": (
                    {
                        "id": str(row.target_user_id),
                        "email": row.target_email,
                    }
                    if row.target_user_id
                    else None
                ),
                "details": json.loads(row.details) if row.details else None,
                "reason": row.reason,
                "created_at": row.created_at.isoformat() if row.created_at else None,
            }
            for row in rows
        ],
    }
