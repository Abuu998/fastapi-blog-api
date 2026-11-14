from datetime import UTC, datetime, timedelta
import jwt
from typing import Annotated
from fastapi import Depends
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer
from pwdlib import PasswordHash
from config import settings


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
cookie_scheme = APIKeyCookie(name="refresh_token")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


# Create access Token
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.ACCESS_TOKEN_SECRET.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


# Create refresh Token
def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            seconds=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.REFRESH_TOKEN_SECRET.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


# Verify access token
def verify_access_token(token: str) -> str | None:
    """Verify a JWT access token and return the subject (user_id) if  valid"""
    try:
        payload = jwt.decode(
            token,
            settings.ACCESS_TOKEN_SECRET.get_secret_value(),
            algorithms=settings.ALGORITHM,
            options={"require": ["exp", "sub"]},
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")


# Verify refresh Token
def verify_refresh_token(token: str) -> str | None:
    """Verify a JWT refresh token and return the subject (user_id) if  valid"""
    try:
        payload = jwt.decode(
            token,
            settings.REFRESH_TOKEN_SECRET.get_secret_value(),
            algorithms=settings.ALGORITHM,
            options={"require": ["exp", "sub"]},
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")

ExtractRefreshToken = Annotated[str, Depends(cookie_scheme)]
