from datetime import datetime

from sqlalchemy import DateTime, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(),
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now(),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {', '.join(f'{k}={v}' for k, v in self.__dict__.items())}>"
