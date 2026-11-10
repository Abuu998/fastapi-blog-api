from __future__ import annotations

from sqlalchemy.orm import Mapped, relationship

from models.users import BaseUser
from models.posts import BasePost


class User(BaseUser):
    posts: Mapped[list[Post]] = relationship(back_populates="author", cascade="all, delete-orphan")


class Post(BasePost):
    author: Mapped[User] = relationship(back_populates="posts")
