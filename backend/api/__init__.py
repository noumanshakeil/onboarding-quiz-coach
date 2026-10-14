from fastapi import APIRouter
from backend.api import health, quiz, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(quiz.router, prefix="/api", tags=["quiz"])
api_router.include_router(ui.router, tags=["ui"])
