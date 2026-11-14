from fastapi import APIRouter, HTTPException, status
from schemas.posts import PostCreate, PostResponse, PostUpdate
from services import posts
from lib.utils import CurrentUser
from db import AsyncDabataseSession


router = APIRouter(tags=["posts"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create(post: PostCreate, current_user: CurrentUser, db: AsyncDabataseSession):
    return await posts.create(current_user.id, post, db)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[PostResponse])
async def find_all(db: AsyncDabataseSession):
    return await posts.find_all(db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def find_one(id: str, db: AsyncDabataseSession):
    post = await posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def update_full(
    id: str, changed: PostCreate, current_user: CurrentUser, db: AsyncDabataseSession
):
    post = await posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resource",
        )

    return await posts.update_full(id, changed, db)


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def update_patch(
    id: str, changed: PostUpdate, current_user: CurrentUser, db: AsyncDabataseSession
):
    post = await posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resource",
        )

    return await posts.update_patch(id, changed, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, current_user: CurrentUser, db: AsyncDabataseSession):
    post = await posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resource",
        )

    return await posts.delete(post, db)
