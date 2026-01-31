from contextlib import asynccontextmanager

from app.api import api_router
from app.core.logger import get_logger, setup_logging
from app.core.settings import settings
from app.db.session import engine, init, ping
from app.services.startup import create_default_roles
from fastapi import FastAPI

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up with DEBUG: %s", settings.app.debug)
    await ping()
    await init()
    await create_default_roles()
    yield
    logger.info("Shutting down...")
    await engine.dispose()
    logger.info("Bye bye!")


app = FastAPI(
    title="Simple Auth Service",
    description="Simple auth service basic on FastAPI",
    version="1.0",
    docs_url="/docs" if settings.app.debug else None,
    redoc_url="/redoc" if settings.app.debug else None,
    openapi_url="/openapi.json" if settings.app.debug else None,
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"status": "ok"}
