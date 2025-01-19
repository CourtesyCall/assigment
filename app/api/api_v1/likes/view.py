from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from api.api_v1.likes.crud import get_likes_by_category, delete_like, create_like
from api.api_v1.likes.schemas import LikeRead, LikeCreate

from db.models.db_helper import db_helper

router = APIRouter(
    tags=["Likes"],
    prefix="/likes",
)


@router.post("", response_model=LikeRead)
async def add_like(
    like_data: LikeCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await create_like(
        session, like_data.user_id, like_data.category_id, like_data.target_id
    )


@router.get("", response_model=list[LikeRead])
async def list_likes(
    category_id: int,
    target_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await get_likes_by_category(session, category_id, target_id)


@router.delete("/{like_id}", response_model=dict)
async def remove_like(
    like_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    result = await delete_like(session, like_id)
    return result
