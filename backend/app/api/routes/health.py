from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    name: str
    version: str


@router.get("/", response_model=HealthResponse)
def get_health():
    return HealthResponse(
        status="healthy",
        name=settings.APP_NAME,
        version=settings.APP_VERSION,
    )
