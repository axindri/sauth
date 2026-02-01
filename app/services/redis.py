from dataclasses import dataclass

from app.core.logger import get_logger
from app.core.settings import settings
from app.db.redis import get_redis
from fastapi import Depends
from redis.asyncio import Redis

ACCESS_KEY_PREFIX = "access"
logger = get_logger(__name__)


@dataclass
class RedisService:
    redis: Redis

    def _key(self, jti: str) -> str:
        return f"{ACCESS_KEY_PREFIX}:{jti}"

    async def set_access_token(self, jti: str, value: str = "1") -> None:
        key = self._key(jti)
        logger.debug("Setting access token: %s", key)
        await self.redis.set(key, value, ex=settings.auth.access_token_expire_seconds)

    async def get_access_token(self, jti: str) -> str | None:
        key = self._key(jti)
        value: bytes | None = await self.redis.get(key)
        logger.debug("Got access token: %s", value)
        return value.decode("utf-8") if value is not None else None

    async def delete_access_token(self, jti: str) -> None:
        key = self._key(jti)
        logger.debug("Deleting access token: %s", key)
        await self.redis.delete(key)


def get_redis_service(redis: Redis = Depends(get_redis)) -> RedisService:
    return RedisService(redis=redis)
