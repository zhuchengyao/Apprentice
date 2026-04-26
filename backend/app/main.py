import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import settings

# Show INFO logs from application code (app.*) while keeping noisy
# third-party loggers (httpx, sqlalchemy, etc.) at WARNING.
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logging.getLogger("app").setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Apprentice",
    description="AI-powered study companion",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
