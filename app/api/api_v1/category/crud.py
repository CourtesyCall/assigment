from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import importlib
from api.api_v1.category.schemas import CategoryCreate
from db.models.likes.category import Category


async def create_category(session: AsyncSession, category: CategoryCreate) -> Category:
    category = Category(name=category.name, model_path=category.model_path)
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
    if category.name is not None:
        category_data.name = category.name
    if category.model_path is not None:
        category_data.model_path = category.model_path

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


# Dev, don't know if it's going to work
async def get_model_from_category(session: AsyncSession, category_id: int):

    result = await session.execute(
        select(Category.model_path).where(Category.id == category_id)
    )
    model_path = result.scalar()
    if not model_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid category"
        )

    try:
        module_path, model_name = model_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        model = getattr(module, model_name)
        return model
    except (ModuleNotFoundError, AttributeError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading model: {e}",
        )


async def target_exists(
    session: AsyncSession, category_id: int, target_id: int
) -> bool:
    model = await get_model_from_category(session, category_id)
    result = await session.execute(select(model).where(model.id == target_id))
    return result.scalar() is not None
