from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES


def _validate_language(v: str) -> str:
    if v not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {v}")
    return v


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    preferred_language: str = DEFAULT_LANGUAGE

    @field_validator("preferred_language")
    @classmethod
    def _check_lang(cls, v: str) -> str:
        return _validate_language(v)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class GoogleAuthRequest(BaseModel):
    code: str


LEARNER_PROFILE_MAX_CHARS = 2000


class UpdateProfileRequest(BaseModel):
    preferred_language: str | None = None
    learner_profile: str | None = None

    @field_validator("preferred_language")
    @classmethod
    def _check_lang(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return _validate_language(v)

    @field_validator("learner_profile")
    @classmethod
    def _check_profile(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if len(v) > LEARNER_PROFILE_MAX_CHARS:
            raise ValueError(
                f"learner_profile must be at most {LEARNER_PROFILE_MAX_CHARS} characters"
            )
        return v


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    avatar_url: str | None = None
    auth_provider: str = "email"
    preferred_language: str = DEFAULT_LANGUAGE
    learner_profile: str | None = None


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
