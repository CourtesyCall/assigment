from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from api.api_v1.category.crud import category_get_by_id, target_exists
from api.api_v1.users.crud import get_user
from core.error_handler import verify_ownership
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

    # if not await target_exists(session, category_id, target_id):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Target with id {target_id} does not exist in category {category.name}",
    #     )

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


async def delete_like(session: AsyncSession, like_id: int, user_id: int) -> None:
    like = await session.get(Like, like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    await verify_ownership(like.user_id, user_id, session)
    await session.delete(like)
    await session.commit()


async def get_likes_service(session: AsyncSession):
    # likes = select(Like).order_by(Like.id)
    # result = await session.scalars(likes)
    # user = get_user(session, likes.c.user_id)

    # Запрос с предзагрузкой данных пользователя и категории
    likes_query = (
        select(Like)
        .options(
            joinedload(Like.user),  # Предзагрузка данных пользователя
            joinedload(Like.category),  # Предзагрузка данных категории
        )
        .order_by(Like.id)
    )
    result = await session.execute(likes_query)
    likes = result.scalars().all()

    # Формируем список словарей
    likes_with_users_and_categories = [
        {
            "like_id": like.id,
            "target_id": like.target_id,
            "category": {
                "id": like.category.id,
                "name": like.category.name,
                "model_path": like.category.model_path,
            },
            "user": {
                "id": like.user.id,
                "username": like.user.username,
                "email": like.user.email,
            },
        }
        for like in likes
    ]

    return {"likes": likes_with_users_and_categories}
