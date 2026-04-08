from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.usage import ApiUsage
from app.services.ai_client import MODEL_PRICING

router = APIRouter()


@router.get("/summary")
async def get_usage_summary(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    """Return aggregated usage and cost, grouped by model and caller."""
    since = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=days)

    result = await db.execute(
        select(
            ApiUsage.model,
            ApiUsage.caller,
            func.count(ApiUsage.id).label("calls"),
            func.sum(ApiUsage.input_tokens).label("input_tokens"),
            func.sum(ApiUsage.output_tokens).label("output_tokens"),
            func.sum(ApiUsage.cost_usd).label("cost_usd"),
        )
        .where(ApiUsage.created_at >= since)
        .group_by(ApiUsage.model, ApiUsage.caller)
        .order_by(func.sum(ApiUsage.cost_usd).desc())
    )
    rows = result.all()

    breakdown = []
    total_cost = 0.0
    total_input = 0
    total_output = 0
    total_calls = 0
    for row in rows:
        cost = float(row.cost_usd or 0)
        inp = int(row.input_tokens or 0)
        out = int(row.output_tokens or 0)
        calls = int(row.calls or 0)
        total_cost += cost
        total_input += inp
        total_output += out
        total_calls += calls
        breakdown.append({
            "model": row.model,
            "caller": row.caller,
            "calls": calls,
            "input_tokens": inp,
            "output_tokens": out,
            "cost_usd": round(cost, 6),
        })

    return {
        "period_days": days,
        "total_calls": total_calls,
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_cost_usd": round(total_cost, 6),
        "breakdown": breakdown,
    }


@router.get("/recent")
async def get_recent_usage(
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """Return the most recent individual API calls."""
    result = await db.execute(
        select(ApiUsage)
        .order_by(ApiUsage.created_at.desc())
        .limit(limit)
    )
    rows = result.scalars().all()

    return {
        "records": [
            {
                "id": str(r.id),
                "model": r.model,
                "provider": r.provider,
                "caller": r.caller,
                "input_tokens": r.input_tokens,
                "output_tokens": r.output_tokens,
                "cost_usd": round(r.cost_usd, 6),
                "created_at": r.created_at.isoformat(),
            }
            for r in rows
        ]
    }


@router.get("/pricing")
async def get_pricing():
    """Return the current pricing table."""
    return {
        "unit": "USD per 1M tokens",
        "models": {
            model: {"input": p["input"], "output": p["output"]}
            for model, p in MODEL_PRICING.items()
        },
    }
