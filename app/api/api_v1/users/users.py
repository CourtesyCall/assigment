from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from fastapi.params import Query
from pydantic import EmailStr
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
    get_user_by_name,
    get_user_by_email,
)

from .schemas import UserRead, UserCreate, UserUpdate, UserSearchSchema
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


@router.get(
    "/pagination",
    summary="Get a paginated list of users",
)
async def get_users_pag(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    print("check 0")
    users = await get_all_users_pag(session=session, skip=skip, limit=limit)

    return users


# @router.get(
#     "/search",
#     summary="Search users by username or email",
# )
async def search_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: UserSearchSchema,
):
    user = await search_users_by_username_or_email(
        session=session, username=user.username, email=user.email
    )
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
    "/name/{user_name}", response_model=UserRead, summary="Get a user's data by Name"
)
async def get_user_by_id(
    user_name: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await get_user_by_name(session=session, name=user_name)
    return user


@router.get(
    "/email/{email}", response_model=UserRead, summary="Get a user's data by Email"
)
async def get_user_by_id(
    email: EmailStr,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await get_user_by_email(session=session, email=email)
    return user


@router.put("/dev/{user_id}", response_model=dict, summary="Make user be admin by ID")
async def make_user_admin(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
):
    return await user_admin_update(session=session, user_id=user_id)
