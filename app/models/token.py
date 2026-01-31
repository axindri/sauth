from datetime import datetime, timedelta

from app.core.settings import settings
from app.models.base import Base
from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
    token: Mapped[str] = mapped_column(String(1024))
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now() + timedelta(seconds=settings.auth.refresh_token_expire_seconds),
    )
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)


class RequestToken(Base):
    __tablename__ = "request_tokens"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    type: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
    code: Mapped[str] = mapped_column(String(16))
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now() + timedelta(seconds=settings.auth.request_token_expire_seconds),
    )
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint(
            "type",
            "user_id",
            "code",
            name="uix_request_token_type_user_id_code",
        ),
    )
