from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from api.api_v1.category.crud import category_get_by_id
from db.models.likes.like import Like
from fastapi import HTTPException, status


async def create_like(
    session: AsyncSession, user_id: int, category_id: int, target_id: int
) -> Like:
    category = await category_get_by_id(session, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist",
        )

    like = Like(user_id=user_id, category_id=category_id, target_id=target_id)
    session.add(like)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate like"
        )
    await session.refresh(like)
    return like


async def get_likes_by_category(
    session: AsyncSession, category_id: int, target_id: int
) -> Sequence[Like]:
    query = select(Like).where(
        Like.category_id == category_id, Like.target_id == target_id
    )
    result = await session.execute(query)
    return result.scalars().all()


async def delete_like(session: AsyncSession, like_id: int) -> None:
    like = await session.get(Like, like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    await session.delete(like)
    await session.commit()
