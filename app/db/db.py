from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from app.core.exceptions import UnexpectedErrorException
from app.core.logger import get_logger
from app.core.settings import settings
from app.models import Base
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

logger = get_logger(__name__)

engine = create_async_engine(
    settings.database.url,
    echo=settings.app.debug,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker[AsyncSession](
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception as e:
            await session.rollback()
            raise UnexpectedErrorException(detail="Failed to get database session", error=e)
        finally:
            await session.close()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception as e:
            await session.rollback()
            raise UnexpectedErrorException(detail="Failed at database transaction", error=e)
        finally:
            await session.close()


async def ping() -> bool:
    try:
        async with AsyncSession(engine) as session:
            await session.execute(text("SELECT 1"))
            logger.info("Database connection established successfully")
            return True
    except Exception as e:
        logger.error("Failed to ping database: %s", e)
        return False


async def init() -> None:
    async with engine.begin() as conn:
        logger.info("Initializing database...")
        await conn.run_sync(Base.metadata.create_all)
