from uuid import uuid4

from app.core.constants import Role
from app.db.db import get_session
from app.models import Role as RoleModel
from sqlalchemy import select


async def create_default_roles():
    async with get_session() as session:
        for role in Role:
            role_model = RoleModel(id=uuid4(), name=role.value, description=role.description)
            if not (await session.execute(select(RoleModel).where(RoleModel.name == role.value))).scalar_one_or_none():
                session.add(role_model)
