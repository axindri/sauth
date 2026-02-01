from collections.abc import AsyncGenerator

from app.core.exceptions import UnexpectedErrorException
from app.core.settings import settings
from fastapi import HTTPException
from redis.asyncio import Redis

redis = Redis.from_url(settings.redis.url)


async def get_redis() -> AsyncGenerator[Redis, None]:
    try:
        yield redis
    except HTTPException as e:
        raise e
    except Exception as e:
        raise UnexpectedErrorException(detail="Failed to get Redis", error=e)
