from uuid import UUID

from app.core.constants import Role
from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: Role
    is_verified: bool
    data: dict

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    name: str
    is_verified: bool
    data: dict
