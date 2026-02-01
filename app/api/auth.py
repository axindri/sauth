from uuid import uuid4

from app.core.constants import Role
from app.core.exceptions import BadRequestException, NotFoundException, UnauthorizedException
from app.core.logger import get_logger
from app.core.security import PasswordManager
from app.db.db import get_session
from app.dependencies.current_context import get_current_token, get_current_user
from app.models import LoginHistory
from app.models import RefreshToken as RefreshTokenModel
from app.models import Role as RoleModel
from app.models import User as UserModel
from app.schemas import LoginRequest, MessageResponse, RefreshTokenRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.db import DbService, get_db_service
from app.services.jwt import JwtService, get_jwt_service
from app.services.redis import RedisService, get_redis_service
from app.services.token import TokenService, get_token_service
from fastapi import APIRouter, Depends, Request

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

password_manager = PasswordManager()


@router.post("/register")
async def register(
    register_request: RegisterRequest,
    db: DbService = Depends(get_db_service),
) -> MessageResponse:
    register_request_data = register_request.model_dump(exclude={"password"})
    register_request_data["password"] = password_manager.hash(register_request.password)
    async with get_session() as session:
        role = await db.get_first(session, RoleModel, name=Role.user.value)
        if not role:
            raise NotFoundException(detail="Role user not found")
        db_user = await db.get_one_or_none(session, UserModel, email=register_request.email)
        if db_user:
            raise BadRequestException(detail="User with this email already exists")
        await db.create(session, UserModel, **register_request_data, id=uuid4(), role_id=role.id)
    return MessageResponse(message="User created successfully")


@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request,
    login_request: LoginRequest,
    db: DbService = Depends(get_db_service),
    token_service: TokenService = Depends(get_token_service),
):
    async with get_session() as session:
        user = await db.get_first(session, UserModel, email=login_request.email)
        if not user:
            logger.error("User not found: %s", login_request.email)
            raise UnauthorizedException(detail="Invalid credentials")
        if not password_manager.verify(login_request.password, user.password):
            logger.error("Invalid password for user: %s", login_request.email)
            raise UnauthorizedException(detail="Invalid credentials")
        access_token, refresh_token = await token_service.issue_tokens(session, user.id)
        ip_address = request.client.host if request.client else ""
        user_agent = request.headers.get("user-agent", "")
        await db.create(
            session,
            LoginHistory,
            id=uuid4(),
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/me")
async def me(user: UserModel = Depends(get_current_user), db: DbService = Depends(get_db_service)):
    async with get_session() as session:
        user_role = await db.get_one_or_none(session, RoleModel, id=user.role_id)
        if not user_role:
            raise NotFoundException(detail="Role not found")
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            role=Role[user_role.name],
            is_verified=user.is_verified,
            data=user.data,
        )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    refresh_token_request: RefreshTokenRequest,
    access_token: str = Depends(get_current_token),
    redis_service: RedisService = Depends(get_redis_service),
    jwt_service: JwtService = Depends(get_jwt_service),
    db: DbService = Depends(get_db_service),
) -> MessageResponse:
    payload = jwt_service.decode(access_token)
    jti = payload.get("jti")
    if jti:
        async with get_session() as session:
            await redis_service.delete_access_token(jti)
            record = await db.get_one_or_none(session, RefreshTokenModel, token=refresh_token_request.refresh_token)
            if record:
                await db.update(session, record, is_used=True)
    return MessageResponse(message="Logged out successfully")
