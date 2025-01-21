from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.comments.crud import (
    get_comments,
    create_comment,
    delete_comment,
    update_comment_service,
)
from api.api_v1.comments.schemas import CommentSchema, CommentUpdate
from api.api_v1.users.schemas import UserRead
from api.auth.auth import get_current_active_auth_user
from db.models.db_helper import db_helper

router = APIRouter(
    tags=["Comments"],
    prefix="/comments",
)


@router.get("", summary="Get a list of all comments")
async def list_comments(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await get_comments(session)


@router.post("", summary="Create a new comment")
async def create_new_comment(
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    comment_create: CommentSchema,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await create_comment(session, comment_create, user.id)


@router.put("/{comment_id}", summary="Update a comment")
async def update_comment(
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    comment_update: CommentUpdate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await update_comment_service(session, comment_update, user.id)


@router.delete("/{comment_id}", summary="Delete a comment")
async def delete_existing_comment(
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    comment_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await delete_comment(session, comment_id, user.id)
