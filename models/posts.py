from datetime import UTC, datetime

from sqlalchemy import DateTime, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import Base

from lib import utils


class BasePost(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(
        Text, 
        primary_key=True, 
        default=utils.generate_id,
        index=True, 
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=UTC), 
        default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=UTC), 
        default=lambda: datetime.now(UTC)
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
