from uuid import uuid4

from app.core.constants import Role
from app.core.exceptions import BadRequestException, NotFoundException, UnauthorizedException
from app.core.logger import get_logger
from app.core.security import PasswordManager
from app.db.session import get_session
from app.models import Role as RoleModel
from app.models import User as UserModel
from app.schemas import LoginRequest, MessageResponse, RegisterRequest
from app.services.db import DbService, get_db_service
from fastapi import APIRouter, Depends

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

password_manager = PasswordManager()


@router.post("/register")
async def register(register_request: RegisterRequest, db: DbService = Depends(get_db_service)) -> MessageResponse:
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


@router.post("/login")
async def login(login_request: LoginRequest, db: DbService = Depends(get_db_service)) -> MessageResponse:
    async with get_session() as session:
        user = await db.get_first(session, UserModel, email=login_request.email)
        if not user:
            logger.error(f"User not found: {login_request.email}")
            raise UnauthorizedException(detail="Invalid credentials")
        if not password_manager.verify(login_request.password, user.password):
            logger.error(f"Invalid password for user: {login_request.email}")
            raise UnauthorizedException(detail="Invalid credentials")
    return MessageResponse(message="User logged in successfully")


@router.get("/me")
def me():
    return {"message": "ok"}


@router.post("/logout")
def logout():
    return {"message": "ok"}
