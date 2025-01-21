from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.db_helper import db_helper
from .crud import (
    get_all_users,
    create_user_one,
    put_user_one,
    user_delete_id,
    get_user,
    search_users_by_username_or_email,
    get_all_users_pag,
    user_admin_update,
)

from .schemas import UserRead, UserCreate, UserUpdate
from ...auth.auth import get_current_active_auth_user

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@router.get("", response_model=list[UserRead], summary="Get a list of all users")
async def get_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    users = await get_all_users(session=session)
    return users


@router.post("/create", response_model=UserRead, summary="Create a new user")
async def create_user(
    user_create: UserCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await create_user_one(session=session, user_create=user_create)
    user.password = user.password.decode("utf-8")
    return user


@router.put("/{user_id}", response_model=UserRead, summary="Update a user's data by ID")
async def update_user(
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    user_update: UserUpdate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await put_user_one(session=session, user_id=user.id, user_update=user_update)

    return user


@router.delete("/{user_id}", response_model=dict, summary="Delete a user's data by ID")
async def delete_user(
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    result = await user_delete_id(session=session, user_id=user.id)
    return result


@router.get("/{user_id}", response_model=UserRead, summary="Get a user's data by ID")
async def get_user_by_id(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await get_user(session=session, user_id=user_id)
    return user


@router.get(
    "/search",
    response_model=list[UserRead],
    summary="Search users by username or email",
)
async def search_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    username: Optional[str] = None,
    email: Optional[str] = None,
):
    user = await search_users_by_username_or_email(
        session=session, username=username, email=email
    )
    return user


@router.get(
    "/pagination",
    response_model=list[UserRead],
    summary="Get a paginated list of users",
)
async def get_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    skip: int = 0,
    limit: int = 10,
):
    users = await get_all_users_pag(session=session, skip=skip, limit=limit)
    return users


@router.put("/dev/{user_id}", response_model=dict, summary="Make user be admin by ID")
async def make_user_admin(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
):
    return await user_admin_update(session=session, user_id=user_id)
