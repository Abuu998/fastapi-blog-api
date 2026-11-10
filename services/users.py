from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.users import UserResponse, UserCreate, UserUpdate

from models import User, Post


def create(user: UserCreate, db: Session) -> UserResponse:
    new_user = User(
        name=user.name,
        email=user.email,
        username=user.username
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def find_all(db: Session) -> list[UserResponse]:
    result = db.execute(select(User))
    users = result.scalars().all()

    return users


def find_one(id: str, db: Session) -> UserResponse | None:
    result = db.execute(select(User).where(User.id == id))
    user = result.scalars().first()

    return user


def patch(user: UserResponse, changed: UserUpdate, db: Session) -> UserResponse:
    update_data = changed.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def find_posts(id: str, db:Session) -> list[Post]:
    result = db.execute(select(Post).where(Post.user_id == id))
    user_posts = result.scalars().all()

    return user_posts


def delete(user: UserResponse, db: Session):
    db.delete(user)
    db.commit()