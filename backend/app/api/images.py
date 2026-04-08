from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import settings

router = APIRouter()

_IMAGES_ROOT = Path(settings.upload_dir).resolve() / "images"


@router.get("/{book_id}/{filename}")
async def get_image(book_id: str, filename: str):
    image_path = (_IMAGES_ROOT / book_id / filename).resolve()
    # Ensure the resolved path is still under the images root
    if not image_path.is_relative_to(_IMAGES_ROOT):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)
