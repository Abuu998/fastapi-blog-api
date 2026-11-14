from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import UserPrivate
from schemas.utils import Token
from datetime import timedelta
from typing import Annotated
from lib.auth import (
    ExtractRefreshToken,
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_refresh_token,
)
from config import settings
from db import AsyncDabataseSession
from sqlalchemy import select, func
from models import User
from services import users
from lib.utils import CurrentUser


router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: AsyncDabataseSession,
):
    # Note: OAuth2PasswordRequestForm uses "username" field, we will use it as "email"
    result = await db.execute(
        select(User).where(func.lower(User.email) == form_data.username.lower())
    )
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create Access and Refresh Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.id}, expires_delta=refresh_token_expires
    )

    # Set Cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # Blocks JavaScript access (prevents XSS)
        # secure=True,          # Sends cookie only over HTTPS (set False for local HTTP testing)
        # samesite="lax",       # Mitigates CSRF attacks ("strict" or "lax")
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES,  # Expiration time in 7 days
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/refresh", response_model=Token)
async def refresh(
    response: Response, refresh_token: ExtractRefreshToken, db: AsyncDabataseSession
):
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify_refresh_token(refresh_token)

    if user_id is None:
        raise unauthorized_exception

    user = await users.find_one(user_id, db)

    if not user:
        raise unauthorized_exception

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    new_refresh_token = create_refresh_token(
        data={"sub": user.id}, expires_delta=refresh_token_expires
    )

    # Set Cookies
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,  # Blocks JavaScript access (prevents XSS)
        # secure=True,          # Sends cookie only over HTTPS (set False for local HTTP testing)
        # samesite="lax",       # Mitigates CSRF attacks ("strict" or "lax")
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES,  # Expiration time in 7 days
    )

    return Token(access_token=new_access_token, token_type="bearer")


@router.get("/me", response_model=UserPrivate)
async def loggedin_user(current_user: CurrentUser):
    return current_user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="refresh_token", httponly=True)
