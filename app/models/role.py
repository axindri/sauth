from app.models.base import Base
from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255))
