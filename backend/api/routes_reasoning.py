from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Reasoning"])


@router.post("/reason")
async def reason():
    return {"message": "Phase 0 skeleton: reasoning endpoint ready for Phase 6 pipeline integration"}
