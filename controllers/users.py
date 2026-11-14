from fastapi import APIRouter, status, HTTPException
from schemas.users import UserPrivate, UserCreate, UserUpdate, UserPublic
from schemas.posts import PostResponse
from services import users
from lib.utils import CurrentUser
from db import AsyncDabataseSession


router = APIRouter(tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserPrivate)
async def create(user: UserCreate, db: AsyncDabataseSession):
    exist_user = await users.find_user_by_username(user.username, db)

    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    exist_user = await users.find_user_by_email(user.email, db)

    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    return await users.create(user, db)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[UserPublic])
async def find_all(db: AsyncDabataseSession):
    return await users.find_all(db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def find_one(id: str, db: AsyncDabataseSession):
    user = await users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    return user


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=UserPrivate)
async def patch(
    id: str, changed: UserUpdate, current_user: CurrentUser, db: AsyncDabataseSession
):
    user = await users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to change this resource",
        )

    update_data = changed.model_dump(exclude_unset=True)

    if update_data.email:
        user = await users.find_user_by_email(update_data.email, db)

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
            )

    if update_data.username:
        user = await users.find_user_by_username(update_data.username, db)

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            )

    return await users.patch(user, update_data, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, current_user: CurrentUser, db: AsyncDabataseSession):
    user = await users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this resource",
        )

    return await users.delete(user, db)


@router.get(
    "/{id}/posts", status_code=status.HTTP_200_OK, response_model=list[PostResponse]
)
async def find_all_posts(id: str, db: AsyncDabataseSession):
    user = await users.find_one(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    return await users.find_posts(user.id, db)
