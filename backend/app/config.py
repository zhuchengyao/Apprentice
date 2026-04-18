from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://apprentice:apprentice@localhost:5432/apprentice"
    redis_url: str = "redis://localhost:6379"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    ai_model: str = "claude-sonnet-4-6"  # must match a model in MODEL_REGISTRY
    tutor_model: str = "gpt-5.4"  # model used for the tutor/teaching system
    upload_dir: str = "./uploads"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Auth
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 10080  # 7 days

    # Google OAuth (optional)
    google_client_id: str = ""
    google_client_secret: str = ""
    frontend_url: str = "http://localhost:3000"

    # Stripe
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""

    model_config = {"env_file": "../.env", "extra": "ignore"}


settings = Settings()
