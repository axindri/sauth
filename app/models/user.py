from app.models.base import Base
from sqlalchemy import UUID, Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(1024))
    name: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("roles.id"))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    data: Mapped[dict] = mapped_column(JSONB, default={})
