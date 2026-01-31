from app.models.base import Base
from sqlalchemy import UUID, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class Social(Base):
    __tablename__ = "socials"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    provider: Mapped[str] = mapped_column(String(255))
    provider_user_id: Mapped[str] = mapped_column(String(255))
    data: Mapped[dict] = mapped_column(JSONB, default={})

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_user_id",
            name="uix_social_provider_user_id",
        ),
    )
