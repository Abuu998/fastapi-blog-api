from fastapi import APIRouter, status, Depends, HTTPException
from schemas.users import UserResponse, UserCreate, UserUpdate
from schemas.posts import PostResponse
from services import users

from typing import Annotated

from db import get_db

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
async def create(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(User.username == user.username))
    exist_user = result.scalars().first()

    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    result = await db.execute(select(User).where(User.email == user.email))
    exist_user = result.scalars().first()

    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    return await users.create(user, db)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse]
)
async def find_all(db: Annotated[AsyncSession, Depends(get_db)]):
    return await users.find_all(db)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def find_one(id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await users.find_one(id, db)

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
async def patch(id: str, changed: UserUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return await users.patch(user, changed, db)



@router.delete(
    "/{id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return await users.delete(user, db)



@router.get(
    "/{id}/posts",
    status_code=status.HTTP_200_OK,
    response_model=list[PostResponse]
)
async def find_all_posts(id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    return await users.find_posts(user.id, db)
