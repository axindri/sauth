from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.models import RefreshToken
from app.services.db import DbService, get_db_service
from app.services.jwt import JwtService, get_jwt_service
from app.services.redis import RedisService, get_redis_service
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class TokenService:
    db: DbService
    redis_service: RedisService
    jwt_service: JwtService

    async def issue_tokens(
        self,
        session: AsyncSession,
        user_id: UUID,
    ) -> tuple[str, str]:
        sub = str(user_id)
        access_token, refresh_token = self.jwt_service.create_pair(sub)

        access_payload = self.jwt_service.decode(access_token)
        await self.redis_service.set_access_token(access_payload["jti"])

        refresh_payload = self.jwt_service.decode(refresh_token)
        expires_at = datetime.fromtimestamp(refresh_payload["exp"], tz=UTC).replace(tzinfo=None)

        await self.db.create(
            session,
            RefreshToken,
            id=uuid4(),
            user_id=user_id,
            token=refresh_token,
            expires_at=expires_at,
        )

        return access_token, refresh_token


def get_token_service(
    db: DbService = Depends(get_db_service),
    redis_service: RedisService = Depends(get_redis_service),
    jwt_service: JwtService = Depends(get_jwt_service),
) -> TokenService:
    return TokenService(db=db, redis_service=redis_service, jwt_service=jwt_service)
