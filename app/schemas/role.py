from uuid import UUID

from pydantic import BaseModel


class RoleResponse(BaseModel):
    id: UUID
    name: str
    description: str

    class Config:
        from_attributes = True
