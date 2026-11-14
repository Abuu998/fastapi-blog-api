from uuid import uuid4
from datetime import UTC, datetime, timedelta
import jwt
from typing import Annotated
from db import AsyncDabataseSession
from lib.auth import verify_access_token, oauth2_scheme
from schemas.users import UserPrivate
from services import users
from fastapi import status, Depends, HTTPException


def generate_id() -> str:
    return uuid4().hex


async def get_current_user(
    access_token: Annotated[str, Depends(oauth2_scheme)], db: AsyncDabataseSession
) -> UserPrivate:
    """Get Currently authenticated user."""
    user_id = verify_access_token(access_token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await users.find_one(user_id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user found!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


CurrentUser = Annotated[UserPrivate, Depends(get_current_user)]