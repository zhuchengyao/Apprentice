from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://apprentice:apprentice@localhost:5432/apprentice"
    redis_url: str = "redis://localhost:6379"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    ai_model: str = "claude-sonnet-4-6"  # must match a model in MODEL_REGISTRY
    tutor_model: str = "gpt-5.4"  # model used for the tutor/teaching system
    illustration_model: str | None = "gpt-5.4"                     # Fallback for any illustration stage that doesn't have a per-stage override below
    illustration_planner_model: str | None = "gpt-5.4"             # Stage 1 — pedagogical scene plan (markdown)
    illustration_spec_model: str | None = "gpt-5.4"                # Stage 2 — JSON SceneSpec (constrained schema)
    illustration_codegen_model: str | None = "claude-sonnet-4-6"   # Stage 3 — Manim Python code
    illustration_embedding_model: str = "text-embedding-3-small"  # retrieval of Manim examples; OpenAI only — Anthropic has no embeddings endpoint
    illustration_qc_enabled: bool = True                           # after render, run a vision-LLM review on the last frame; retry codegen on major layout issues
    illustration_qc_model: str | None = "gpt-5.4"                  # vision-capable model for the QC step; ~$0.005-0.01 per call (full gpt-5.4 catches subtler layout issues than mini)
    illustration_qc_severity_threshold: str = "major"              # "minor" | "major" — minimum severity that triggers a codegen retry
    illustration_qc_retries: int = 1                                # hard cap on QC-driven retries per KP
    prewarm_scope_explanations: bool = False  # parse-stage: generate scope EXPLAIN text up-front so first-student latency is zero. Costs one tutor LLM call per scope.
    prewarm_language: str = "en"                # language used when pre-warming explanations
    manim_python: str | None = None  # python interpreter used to run `manim`; falls back to backend/.venv/bin/python or sys.executable
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
