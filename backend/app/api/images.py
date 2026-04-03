import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import settings

router = APIRouter()


@router.get("/{book_id}/{filename}")
async def get_image(book_id: str, filename: str):
    # Sanitize to prevent path traversal
    if ".." in book_id or ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Invalid path")

    image_path = os.path.join(settings.upload_dir, "images", book_id, filename)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)
