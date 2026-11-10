from fastapi import APIRouter, status, Depends, HTTPException
from schemas.users import UserResponse, UserCreate, UserUpdate
from schemas.posts import PostResponse
from services import users

from typing import Annotated

from db import get_db

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def create(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(User).where(User.username == user.username))
    exist_user = result.scalars().first()

    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    result = db.execute(select(User).where(User.email == user.email))
    exist_user = result.scalars().first()

    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    return users.create(user, db)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse]
)
def find_all(db: Annotated[Session, Depends(get_db)]):
    return users.find_all(db)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
def find_one(id: str, db: Annotated[Session, Depends(get_db)]):
    user = users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    return user


@router.patch(
    "/{id}", 
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
def patch(id: str, changed: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    user = users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return users.patch(user, changed, db)



@router.delete(
    "/{id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
def delete(id: str, db: Annotated[Session, Depends(get_db)]):
    user = users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return users.delete(user, db)



@router.get(
    "/{id}/posts",
    status_code=status.HTTP_200_OK,
    response_model=list[PostResponse]
)
def find_all_posts(id: str, db: Annotated[Session, Depends(get_db)]):
    user = users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    return users.find_posts(user.id, db)
