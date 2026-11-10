from fastapi import APIRouter, HTTPException, status, Depends
from schemas.posts import PostCreate, PostResponse, PostUpdate

from services import posts, users

from typing import Annotated 

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.post(
    "", 
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponse
)
async def create(post: PostCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    author = await users.find_one(post.user_id, db)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author not found!"
        )

    return await posts.create(post, db)


@router.get(
    "", 
    status_code=status.HTTP_200_OK,
    response_model=list[PostResponse]
)
async def find_all(db: Annotated[AsyncSession, Depends(get_db)]):
    return await posts.find_all(db)


@router.get(
    "/{id}", 
    status_code=status.HTTP_200_OK,
    response_model=PostResponse
)
async def find_one(id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return post


@router.put(
    "/{id}", 
    status_code=status.HTTP_200_OK,
    response_model=PostResponse
)
async def update_full(id: str, changed: PostCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return await posts.update_full(id, changed, db)


@router.patch(
    "/{id}", 
    status_code=status.HTTP_200_OK,
    response_model=PostResponse
)
async def update_patch(id: str, changed: PostUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return await posts.update_patch(id, changed, db)


@router.delete(
    "/{id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return await posts.delete(post, db)
