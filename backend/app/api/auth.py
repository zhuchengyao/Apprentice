"""Authentication API endpoints."""

import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import hash_password, verify_password, create_access_token
from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    GoogleAuthRequest,
    AuthResponse,
    UpdateProfileRequest,
    UserResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


def _user_response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        avatar_url=user.avatar_url,
        auth_provider=user.auth_provider,
        preferred_language=user.preferred_language,
        learner_profile=user.learner_profile,
    )


def _auth_response(user: User) -> AuthResponse:
    token = create_access_token(str(user.id))
    return AuthResponse(
        access_token=token,
        user=_user_response(user),
    )


@router.post("/register", response_model=AuthResponse)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Validate password
    if len(body.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    # Check existing user
    result = await db.execute(select(User).where(User.email == body.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=body.email,
        name=body.name,
        password_hash=hash_password(body.password),
        auth_provider="email",
        preferred_language=body.preferred_language,
    )
    db.add(user)
    await db.flush()

    # Initialize billing: free plan + signup bonus credits
    from app.services.billing import ensure_user_billing
    await ensure_user_billing(db, user.id)

    await db.commit()
    await db.refresh(user)

    return _auth_response(user)


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    return _auth_response(user)


@router.post("/google", response_model=AuthResponse)
async def google_auth(body: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):
    """Exchange Google authorization code for user info, create or find user."""
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=501, detail="Google OAuth not configured")

    # Exchange code for tokens
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": body.code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": f"{settings.frontend_url}/api/auth/google/callback",
                "grant_type": "authorization_code",
            },
        )
        if token_res.status_code != 200:
            logger.error("Google token exchange failed: %s", token_res.text)
            raise HTTPException(status_code=400, detail="Failed to exchange Google auth code")

        tokens = token_res.json()
        access_token = tokens.get("access_token")

        # Get user info
        user_info_res = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if user_info_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get Google user info")

        google_user = user_info_res.json()

    google_id = google_user.get("id")
    email = google_user.get("email")
    name = google_user.get("name", email)
    avatar = google_user.get("picture")

    # Find by google_id first, then by email
    result = await db.execute(select(User).where(User.google_id == google_id))
    user = result.scalar_one_or_none()

    if user:
        if avatar:
            user.avatar_url = avatar

    if not user:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user:
            # Link Google to existing account
            user.google_id = google_id
            if avatar:
                user.avatar_url = avatar
            user.auth_provider = "google"
        else:
            # Create new user
            user = User(
                email=email,
                name=name,
                google_id=google_id,
                avatar_url=avatar,
                auth_provider="google",
            )
            db.add(user)
            await db.flush()

            # Initialize billing: free plan + signup bonus credits
            from app.services.billing import ensure_user_billing
            await ensure_user_billing(db, user.id)

    await db.commit()
    await db.refresh(user)

    return _auth_response(user)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return _user_response(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    body: UpdateProfileRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile_changed = False
    if body.preferred_language is not None:
        current_user.preferred_language = body.preferred_language
    if body.learner_profile is not None:
        current_user.learner_profile = body.learner_profile.strip() or None
        profile_changed = True

    if profile_changed:
        # Invalidate per-student block cache on all this user's tutor
        # conversations so the next turn rebuilds with the updated profile.
        from app.models.tutor import TutorConversation
        await db.execute(
            update(TutorConversation)
            .where(TutorConversation.user_id == current_user.id)
            .values(student_block_cache=None)
        )

    await db.commit()
    await db.refresh(current_user)
    return _user_response(current_user)
