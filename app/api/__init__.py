from app.api.auth import router as auth_router
from app.api.service import router as service_router
from app.api.token import router as token_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(token_router)
api_router.include_router(service_router)
