from fastapi import HTTPException, status
from typing import Sequence, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.comments.schemas import CommentSchema
from db.models.comments.comment import Comment


async def get_comments(session: AsyncSession) -> Sequence[Comment]:
    comments = select(Comment).order_by(Comment.id)
    result = await session.scalars(comments)
    return result.all()


async def create_comment(
    session: AsyncSession, comment_create: CommentSchema
) -> Comment:
    comment = Comment(
        content=comment_create.content,
        blog_id=comment_create.blog_id,
        author_id=comment_create.author_id,
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


async def delete_comment(session: AsyncSession, comment_id: int):
    comment = await get_comment_by_id(session, comment_id)
    if comment:
        await session.delete(comment)
        await session.commit()

    return {"message": f"Comment with ID {comment_id} has been deleted."}


async def get_comment_by_id(session: AsyncSession, comment_id: int) -> Comment:
    comment = await session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return comment
