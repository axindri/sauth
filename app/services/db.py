from dataclasses import dataclass
from typing import Any, TypeVar

from app.models.base import Base
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=Base)


@dataclass
class DbService:
    async def create(self, session: AsyncSession, model: type[T], **kwargs: Any) -> T:
        instance = model(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def get_by_id(self, session: AsyncSession, model: type[T], id: Any) -> T | None:
        return await session.get(model, id)

    async def get_one_or_none(self, session: AsyncSession, model: type[T], **kwargs: Any) -> T | None:
        if not kwargs:
            return None
        conditions = [getattr(model, key) == value for key, value in kwargs.items()]
        stmt = select(model).where(and_(*conditions))
        return (await session.execute(stmt)).scalar_one_or_none()

    async def get_all(
        self,
        session: AsyncSession,
        model: type[T],
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[T]:
        stmt = select(model).order_by(getattr(model, "id"))
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_first(self, session: AsyncSession, model: type[T], **kwargs: Any) -> T | None:
        if not kwargs:
            stmt = select(model).order_by(getattr(model, "id")).limit(1)
        else:
            conditions = [getattr(model, key) == value for key, value in kwargs.items()]
            stmt = select(model).where(and_(*conditions)).limit(1)
        return (await session.execute(stmt)).scalar_one_or_none()

    async def update(self, session: AsyncSession, instance: T, **kwargs: Any) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await session.commit()
        await session.refresh(instance)
        return instance


async def get_db_service() -> DbService:
    return DbService()
