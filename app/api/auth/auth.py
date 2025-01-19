from typing import Annotated
from jwt import InvalidTokenError
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.users.crud import get_user, get_user_by_name
from api.api_v1.users.schemas import UserRead
from api.auth.schemas import TokenInfo

from core.utils import encode_jwt, validate_password, decode_jwt
from db.models.db_helper import db_helper


# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/auth/login/")


async def validate_auth_user(
    username: Form,
    password: Form,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    user = await get_user(session, username)
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


def auth_user_jwt(
    user: UserRead = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }
    access_token = encode_jwt(jwt_payload)
    return TokenInfo(access_token=access_token, token_type="Bearer ")


def get_current_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> UserRead:
    # token = credentials.credentials
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
    username: str | None = payload.get("username")
    user = await get_user_by_name(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )
    return user


def get_current_active_auth_user(
    user: UserRead = Depends(get_current_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )
