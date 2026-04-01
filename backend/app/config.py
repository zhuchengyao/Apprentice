from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://apprentice:apprentice@localhost:5432/apprentice"
    redis_url: str = "redis://localhost:6379"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    ai_provider: str = "anthropic"  # "anthropic" or "openai"
    ai_model: str = ""  # override default model, leave empty to use provider default
    upload_dir: str = "./uploads"
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": "../.env", "extra": "ignore"}


settings = Settings()
