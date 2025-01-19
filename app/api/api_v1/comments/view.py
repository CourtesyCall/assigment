from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.comments.crud import get_comments, create_comment, delete_comment
from api.api_v1.comments.schemas import CommentSchema
from db.models.db_helper import db_helper

router = APIRouter(
    tags=["Comments"],
    prefix="/comments",
)


@router.get("")
async def list_comments(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await get_comments(session)


@router.post("")
async def create_new_comment(
    comment_create: CommentSchema,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await create_comment(session, comment_create)


@router.delete("/{comment_id}")
async def delete_existing_comment(
    comment_id: int, session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    await delete_comment(session, comment_id)
    return {"message": "Comment deleted"}
