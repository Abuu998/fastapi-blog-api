from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.posts import PostResponse, PostCreate, PostUpdate

from models import Post


async def create(user_id: str, post: PostCreate, db: AsyncSession) -> PostResponse:
    new_post = Post(title=post.title, content=post.content, user_id=user_id)

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names=["author"])

    return new_post


async def find_all(db: AsyncSession) -> list[PostResponse]:
    result = await db.execute(select(Post).options(selectinload(Post.author)))
    posts = result.scalars().all()

    return posts


async def find_one(id: str, db: AsyncSession) -> PostResponse | None:
    result = await db.execute(
        select(Post).options(selectinload(Post.author)).where(Post.id == id)
    )
    post = result.scalars().first()

    return post


async def update_full(id: str, changed: PostCreate, db: AsyncSession) -> PostResponse:
    post = await find_one(id, db)

    post.title = changed.title
    post.content = changed.content

    await db.commit()
    await db.refresh(post, attribute_names=["author"])

    return post


async def update_patch(id: str, changed: PostUpdate, db: AsyncSession) -> PostResponse:
    post = await find_one(id, db)

    update_data = changed.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post, attribute_names=["author"])

    return post


async def delete(post: PostResponse, db: AsyncSession):
    await db.delete(post)
    await db.commit()
