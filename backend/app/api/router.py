from fastapi import APIRouter
from app.api.books import router as books_router
from app.api.pages import router as pages_router
from app.api.study import router as study_router
from app.api.progress import router as progress_router
from app.api.images import router as images_router
from app.api.usage import router as usage_router

api_router = APIRouter(prefix="/api")
api_router.include_router(books_router, prefix="/books", tags=["books"])
api_router.include_router(pages_router, prefix="/books", tags=["pages"])
api_router.include_router(study_router, prefix="/study", tags=["study"])
api_router.include_router(progress_router, prefix="/progress", tags=["progress"])
api_router.include_router(images_router, prefix="/images", tags=["images"])
api_router.include_router(usage_router, prefix="/usage", tags=["usage"])
