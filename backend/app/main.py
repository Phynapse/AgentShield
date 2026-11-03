from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import health, evaluations, test_suites

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Agent Security & Evaluation Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(test_suites.router, prefix="/test-suites", tags=["test-suites"])
app.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])


@app.get("/")
def root():
    return {"name": settings.APP_NAME, "version": settings.APP_VERSION}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions to prevent leaking internal details."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
