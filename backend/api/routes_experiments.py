from fastapi import APIRouter

router = APIRouter(prefix="/api/experiments", tags=["Experiments"])


@router.get("/")
async def list_experiments():
    return {"experiments": []}
