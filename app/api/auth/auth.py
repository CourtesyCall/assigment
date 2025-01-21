from datetime import timedelta
from typing import Annotated
from jwt import InvalidTokenError
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
    HTTPBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.users.crud import get_user, get_user_by_name, get_user_by_email
from api.api_v1.users.schemas import UserRead, UserLogin, UserAuthSchema
from api.auth.schemas import TokenInfo
from core.config import settings

from core.utils import encode_jwt, validate_password, decode_jwt
from db.models.db_helper import db_helper

http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/auth/login/")

TOKEN_TYPE = "type"
ACCESS_TOKEN_TYPE = "access_token"
REFRESH_TOKEN_TYPE = "refresh_token"


def create_jwt(
    token_type: str,
    payload: dict,
    expires_time: int = settings.auth_jwt.access_token_expires,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE: token_type}
    jwt_payload.update(payload)
    return encode_jwt(
        payload=jwt_payload,
        expire_time=expires_time,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserAuthSchema) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }

    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        payload=jwt_payload,
        expires_time=settings.auth_jwt.access_token_expires,
    )


def create_refresh_token(user: UserAuthSchema) -> str:
    jwt_payload = {"sub": user.username}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        payload=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expires_days),
    )


def validate_token(token_type: str, token: dict) -> bool:
    curren_type = token.get(TOKEN_TYPE)
    if token.get(TOKEN_TYPE) == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {curren_type!r} needs to be {token_type!r}",
    )


async def validate_auth_user(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    user = await get_user_by_name(session, username)
    if not user:
        raise unauthed_exc

    if not validate_password(
        password=password,
        hashed_passw=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active",
        )

    return user


async def auth_user_jwt(
    session: AsyncSession,
    user: UserLogin,
):
    user_data = await get_user_by_email(session, user.email)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    jwt_payload = {
        "sub": user_data.id,
        "username": user_data.username,
        "email": user.email,
        "active": user_data.active,
        "is_admin": user_data.is_admin,
    }
    access_token = encode_jwt(jwt_payload)
    return TokenInfo(access_token=access_token, token_type="Bearer ")


def get_current_payload(
    token: str = Depends(oauth2_scheme),
) -> UserRead:

    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )
    return payload


async def get_current_user(
    payload: dict = Depends(get_current_payload),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserRead:
    validate_token(token=payload, token_type=ACCESS_TOKEN_TYPE)
    username: str | None = payload.get("username")

    user = await get_user_by_name(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )
    return user


async def get_current_user_refresh_token(
    payload: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserRead:

    token = decode_jwt(payload.credentials)
    validate_token(token=token, token_type=REFRESH_TOKEN_TYPE)

    username: str | None = token.get("sub")

    user = await get_user_by_name(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )
    return user


async def get_current_active_auth_user(
    user: UserRead = Depends(get_current_user),
):

    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )
