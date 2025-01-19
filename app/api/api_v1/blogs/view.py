from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.blogs.crud import (
    blog_create_service,
    get_all_blogs,
    blog_update_service,
    blog_delete_service,
)
from api.api_v1.blogs.schemas import BlogRead, BlogCreate
from db.models.db_helper import db_helper


router = APIRouter(
    tags=["Blogs"],
    prefix="/blogs",
)


@router.post("/create", response_model=BlogRead)
async def create_blog(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    blog_create: BlogCreate,
    user_id: int,
):

    result = await blog_create_service(
        session=session, blog=blog_create, author_id=user_id
    )
    return result


@router.get("", response_model=List[BlogRead])
async def get_blogs(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    result = await get_all_blogs(session=session)
    return result


@router.put("/{blog_id}", response_model=BlogCreate)
async def update_blog(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    blog_id: int,
    blog_update: BlogCreate,
):
    result = await blog_update_service(
        session=session,
        blog_id=blog_id,
        blog_update=blog_update,
    )
    return result


@router.delete("/{blog_id}")
async def delete_blog(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    blog_id: int,
):
    result = await blog_delete_service(session=session, blog_id=blog_id)
    return result
