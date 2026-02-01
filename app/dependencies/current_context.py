from app.core.exceptions import UnauthorizedException
from app.core.logger import get_logger
from app.db.db import get_session
from app.models import User as UserModel
from app.services.db import DbService, get_db_service
from app.services.jwt import JwtService, get_jwt_service
from app.services.redis import RedisService, get_redis_service
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

logger = get_logger(__name__)
security = HTTPBearer(auto_error=False)


def get_current_token(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> str:
    token = credentials.credentials if credentials else None
    if not token:
        raise UnauthorizedException(detail="No Bearer token found in Authorization header")
    return token


async def get_current_user(
    token: str = Depends(get_current_token),
    redis_service: RedisService = Depends(get_redis_service),
    jwt_service: JwtService = Depends(get_jwt_service),
    db: DbService = Depends(get_db_service),
) -> UserModel:
    payload = jwt_service.decode(token)
    jti = payload.get("jti")
    if not jti:
        raise UnauthorizedException(detail="Invalid token: missing jti")
    if not await redis_service.get_access_token(jti):
        raise UnauthorizedException(detail="Invalid or expired token")
    async with get_session() as session:
        user = await db.get_one_or_none(session, UserModel, id=payload["sub"])
        if not user:
            raise UnauthorizedException(detail="User not found")
        return user
