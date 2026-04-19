from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.books import router as books_router
from app.api.pages import router as pages_router
from app.api.progress import router as progress_router
from app.api.images import router as images_router
from app.api.usage import router as usage_router
from app.api.tutor import router as tutor_router
from app.api.billing import router as billing_router
from app.api.admin import router as admin_router
from app.api.manim import router as manim_router

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(books_router, prefix="/books", tags=["books"])
api_router.include_router(pages_router, prefix="/books", tags=["pages"])
api_router.include_router(progress_router, prefix="/progress", tags=["progress"])
api_router.include_router(images_router, prefix="/images", tags=["images"])
api_router.include_router(usage_router, prefix="/usage", tags=["usage"])
api_router.include_router(tutor_router, prefix="/tutor", tags=["tutor"])
api_router.include_router(billing_router, prefix="/billing", tags=["billing"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(manim_router, prefix="/manim", tags=["manim"])
