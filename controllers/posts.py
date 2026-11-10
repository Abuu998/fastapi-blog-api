from fastapi import APIRouter, HTTPException, status, Depends
from schemas.posts import PostCreate, PostResponse, PostUpdate

from services import posts, users

from typing import Annotated 

from sqlalchemy.orm import Session

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
def create(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    author = users.find_one(post.user_id, db)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author not found!"
        )

    return posts.create(post, db)


@router.get(
    "", 
    status_code=status.HTTP_200_OK,
    response_model=list[PostResponse]
)
def find_all(db: Annotated[Session, Depends(get_db)]):
    return posts.find_all(db)


@router.get(
    "/{id}", 
    status_code=status.HTTP_200_OK,
    response_model=PostResponse
)
def find_one(id: str, db: Annotated[Session, Depends(get_db)]):
    post = posts.find_one(id, db)

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
def update_full(id: str, changed: PostCreate, db: Annotated[Session, Depends(get_db)]):
    post = posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return posts.update_full(id, changed, db)


@router.patch(
    "/{id}", 
    status_code=status.HTTP_200_OK,
    response_model=PostResponse
)
def update_patch(id: str, changed: PostUpdate, db: Annotated[Session, Depends(get_db)]):
    post = posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return posts.update_patch(id, changed, db)


@router.delete(
    "/{id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
def delete(id: str, db: Annotated[Session, Depends(get_db)]):
    post = posts.find_one(id, db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return posts.delete(post, db)
