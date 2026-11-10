from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserResponse, UserCreate, UserUpdate

from models import User, Post


async def create(user: UserCreate, db: AsyncSession) -> UserResponse:
    new_user = User(
        name=user.name,
        email=user.email,
        username=user.username
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def find_all(db: AsyncSession) -> list[UserResponse]:
    result = await db.execute(select(User))
    users = result.scalars().all()

    return users


async def find_one(id: str, db: AsyncSession) -> UserResponse | None:
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalars().first()

    return user


async def patch(user: UserResponse, changed: UserUpdate, db: AsyncSession) -> UserResponse:
    update_data = changed.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


async def find_posts(id: str, db: AsyncSession) -> list[Post]:
    result = await db.execute(
        select(Post)
        .options(selectinload(Post.author))
        .where(Post.user_id == id)
    )
    user_posts = result.scalars().all()

    return user_posts


async def delete(user: UserResponse, db: AsyncSession):
    await db.delete(user)
    await db.commit()