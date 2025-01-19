from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.category.crud import (
    create_category,
    get_categories,
    delete_category,
    update_category_service,
)
from api.api_v1.category.schemas import CategoryRead, CategoryCreate
from db.models.db_helper import db_helper

router = APIRouter(
    prefix="/category",
    tags=["Category"],
)


@router.post("/", response_model=CategoryRead)
async def create_new_category(
    category: CategoryCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await create_category(session, category.name)


@router.get("/", response_model=list[CategoryRead])
async def list_categories(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await get_categories(session)


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    category_id: int,
    category: CategoryCreate,
):
    return await update_category_service(session, category, category_id)


@router.delete("/{category_id}")
async def delete_existing_category(
    category_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    await delete_category(session, category_id)
    return {"message": "Category deleted"}
