from datetime import UTC, datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from lib.utils import generate_id


class BaseUser(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        Text,
        primary_key=True,
        default=generate_id,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    image_url: Mapped[str | None] = mapped_column(
        String(200), nullable=True, default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=UTC), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=UTC), default=lambda: datetime.now(UTC)
    )
