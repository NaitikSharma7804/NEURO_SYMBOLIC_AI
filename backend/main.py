from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.api.routes_health import router as health_router
from backend.api.routes_reasoning import router as reasoning_router
from backend.api.routes_experiments import router as experiments_router
from backend.api.routes_datasets import router as datasets_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Neuro-Symbolic AI Framework for Automated Logical Reasoning, Theorem Proving, and Explainable Decision Making",
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health_router)
app.include_router(reasoning_router)
app.include_router(experiments_router)
app.include_router(datasets_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
