from typing import List, Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import encode_jwt
from db.models.db_helper import db_helper
from .auth import (
    auth_user_jwt,
    get_current_active_auth_user,
    get_current_payload,
    validate_auth_user,
    create_access_token,
    create_refresh_token,
    get_current_user_refresh_token,
)
from .schemas import TokenInfo
from ..api_v1.users.schemas import UserRead, UserLogin, UserAuthSchema

router = APIRouter(prefix="/auth", tags=["AUTH"])


@router.post("/login/", response_model=TokenInfo)
async def login(
    user: UserAuthSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh/", response_model=TokenInfo, response_model_exclude_none=True)
async def refresh(user: UserAuthSchema = Depends(get_current_user_refresh_token)):
    access_token = create_access_token(user)

    return TokenInfo(access_token=access_token)


@router.get("/users/me/")
async def get_user_auth(
    # payload: dict = Depends(get_current_payload),
    user: UserLogin = Depends(get_current_active_auth_user),
):
    # iat = payload.get("iat")
    return user
