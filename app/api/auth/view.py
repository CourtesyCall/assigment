from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer


from .auth import auth_user_jwt, get_current_active_auth_user
from .schemas import TokenInfo
from ..api_v1.users.schemas import UserRead


router = APIRouter(prefix="/auth", tags=["AUTH"])


@router.post("/login/", response_model=TokenInfo)
async def login(
    user: UserRead,
):
    return await auth_user_jwt(user)


@router.get("/users/me/", response_model=List[UserRead])
def get_user_auth(
    user: UserRead = Depends(get_current_active_auth_user),
):
    return user
