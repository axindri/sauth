from app.models.base import Base
from sqlalchemy import UUID, Index, String
from sqlalchemy.orm import Mapped, mapped_column


class LoginHistory(Base):
    __tablename__ = "login_history"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(UUID, index=True)
    ip_address: Mapped[str] = mapped_column(String(255))
    user_agent: Mapped[str] = mapped_column(String(255))

    __table_args__ = (
        Index(
            "idx_login_history_user_id_ip_address",
            "user_id",
            "ip_address",
        ),
    )
