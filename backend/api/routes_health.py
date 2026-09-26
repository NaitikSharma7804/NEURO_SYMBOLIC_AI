from fastapi import APIRouter
from backend.config.settings import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Health check endpoint for the neuro-symbolic framework."""
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "llm_provider": settings.LLM_PROVIDER,
        "reasoning_backend": settings.REASONING_BACKEND,
    }
