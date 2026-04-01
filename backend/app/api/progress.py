from fastapi import APIRouter

router = APIRouter()


@router.get("/overview")
async def get_overview():
    return {"message": "Progress tracking coming in Phase 4"}
