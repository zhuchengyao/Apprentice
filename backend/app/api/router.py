from fastapi import APIRouter
from app.api.books import router as books_router
from app.api.study import router as study_router
from app.api.progress import router as progress_router

api_router = APIRouter(prefix="/api")
api_router.include_router(books_router, prefix="/books", tags=["books"])
api_router.include_router(study_router, prefix="/study", tags=["study"])
api_router.include_router(progress_router, prefix="/progress", tags=["progress"])
