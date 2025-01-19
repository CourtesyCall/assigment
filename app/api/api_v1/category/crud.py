from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.category.schemas import CategoryCreate
from db.models.likes.category import Category


async def create_category(session: AsyncSession, name: str) -> Category:
    category = Category(name=name)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def get_categories(session: AsyncSession) -> Sequence[Category]:
    categories = select(Category).order_by(Category.id)
    result = await session.scalars(categories)
    return result.all()


async def category_get_by_id(session: AsyncSession, category_id: int):
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    return category


async def update_category_service(
    session: AsyncSession, category: CategoryCreate, category_id: int
):
    category_data = await category_get_by_id(session, category_id)
    if not category_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    category_data.name = category.name
    session.add(category_data)
    await session.commit()
    await session.refresh(category_data)

    return category_data


async def delete_category(session: AsyncSession, category_id: int):
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized or not found"
        )

    await session.delete(category)
    await session.commit()

    return {"message": "Category deleted"}
