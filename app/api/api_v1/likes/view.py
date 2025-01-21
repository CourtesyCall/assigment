from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from api.api_v1.likes.crud import (
    get_likes_by_category,
    delete_like,
    create_like,
    get_likes_service,
)
from api.api_v1.likes.schemas import LikeRead, LikeCreate
from api.api_v1.users.schemas import UserRead
from api.auth.auth import get_current_active_auth_user

from db.models.db_helper import db_helper

router = APIRouter(
    tags=["Likes"],
    prefix="/likes",
)


@router.post("", response_model=LikeRead, summary="Add a like to a category or target")
async def add_like(
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    like_data: LikeCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await create_like(
        session,
        user.id,
        like_data.category_id,
        like_data.target_id,
    )


@router.get("/", summary="Get a list of all likes")
async def get_likes(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await get_likes_service(session)


@router.get(
    "", response_model=list[LikeRead], summary="Get likes by category and target"
)
async def list_likes(
    category_id: int,
    target_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await get_likes_by_category(session, category_id, target_id)


@router.delete("/{like_id}", response_model=dict, summary="Remove a like by ID")
async def remove_like(
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    like_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    result = await delete_like(session, like_id, user.id)
    return result
