from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserPrivate, UserCreate, UserUpdate, UserPublic
from lib.auth import hash_password
import models


async def create(user: UserCreate, db: AsyncSession) -> UserPrivate:
    new_user = models.User(
        name=user.name,
        email=user.email.lower(),
        username=user.username,
        password_hash=hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def find_all(db: AsyncSession) -> list[UserPublic]:
    result = await db.execute(select(models.User))
    users = result.scalars().all()

    return users


async def find_one(id: str, db: AsyncSession) -> UserPublic | None:
    result = await db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()

    return user


async def patch(
    user: UserPrivate, changed: UserUpdate, db: AsyncSession
) -> UserPrivate:
    for field, value in changed.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


async def find_posts(id: str, db: AsyncSession) -> list[models.Post]:
    result = await db.execute(
        select(models.Post).options(selectinload(models.Post.author)).where(models.Post.user_id == id)
    )
    user_posts = result.scalars().all()

    return user_posts


async def delete(user: UserPublic, db: AsyncSession):
    await db.delete(user)
    await db.commit()


async def find_user_by_username(username: str, db: AsyncSession) -> models.User:
    result = await db.execute(
        select(models.User).where(func.lower(models.User.username) == username.lower())
    )
    user = result.scalars().first()

    return user


async def find_user_by_email(email: str, db: AsyncSession) -> models.User:
    result = await db.execute(
        select(models.User).where(func.lower(models.User.email) == email.lower())
    )
    user = result.scalars().first()

    return user
