"""Promote a user to admin (or demote back to 'user') by email.

Usage:
    python -m scripts.promote_admin <email>
    python -m scripts.promote_admin <email> --demote

This is the only supported way to create the first admin. There is no
API endpoint for self-promotion — do not add one.
"""

import argparse
import asyncio
import sys

from sqlalchemy import select

from app.database import async_session
from app.models.user import User


async def main(email: str, demote: bool) -> int:
    new_role = "user" if demote else "admin"

    async with async_session() as db:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            print(f"ERROR: no user found with email {email!r}", file=sys.stderr)
            return 1

        if user.role == new_role:
            print(f"User {email} already has role={new_role!r}. Nothing to do.")
            return 0

        previous = user.role
        user.role = new_role
        await db.commit()

        print(f"OK: {email} role {previous!r} → {new_role!r}")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Promote or demote a user's admin role.")
    parser.add_argument("email", help="Email of the user to promote")
    parser.add_argument(
        "--demote",
        action="store_true",
        help="Set role back to 'user' instead of 'admin'",
    )
    args = parser.parse_args()
    sys.exit(asyncio.run(main(args.email, args.demote)))
