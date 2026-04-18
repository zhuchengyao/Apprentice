"""Admin service: audit logging + user management helpers."""

import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin import AdminAuditLog


async def log_admin_action(
    db: AsyncSession,
    actor_id: uuid.UUID,
    action: str,
    target_user_id: uuid.UUID | None = None,
    details: dict | None = None,
    reason: str | None = None,
) -> None:
    """Append an entry to the admin audit log. Caller is responsible for commit."""
    entry = AdminAuditLog(
        actor_id=actor_id,
        action=action,
        target_user_id=target_user_id,
        details=json.dumps(details) if details else None,
        reason=reason,
    )
    db.add(entry)
