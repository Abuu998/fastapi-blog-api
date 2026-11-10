from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.posts import PostResponse, PostCreate, PostUpdate

from models import Post


def create(post: PostCreate, db: Session) -> PostResponse:
    new_post = Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def find_all(db: Session) -> list[PostResponse]:
    result = db.execute(select(Post))
    posts = result.scalars().all()

    return posts


def find_one(id: str, db: Session) -> PostResponse | None:
    result = db.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()

    return post


def update_full(id: str, changed: PostCreate, db: Session) -> PostResponse:
    post = find_one(id, db)

    post.title = changed.title
    post.content = changed.content

    db.commit()
    db.refresh(post)

    return post


def update_patch(id: str, changed: PostUpdate, db: Session) -> PostResponse:
    post = find_one(id, db)

    update_data = changed.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)

    return post


def delete(post: PostResponse, db: Session):
    db.delete(post)
    db.commit()
