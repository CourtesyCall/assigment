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
from api.api_v1.users.schemas import UserLogin, UserRead
from api.auth.auth import get_current_active_auth_user
from db.models.db_helper import db_helper


router = APIRouter(
    tags=["Blogs"],
    prefix="/blogs",
)


@router.post("/create", response_model=BlogRead, summary="Create a new blog post")
async def create_blog(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    blog_create: BlogCreate,
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
):

    result = await blog_create_service(
        session=session, blog=blog_create, author_id=user.id
    )
    return result


@router.get("", response_model=List[BlogRead], summary="Get a list of all blog posts")
async def get_blogs(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    result = await get_all_blogs(session=session)
    return result


@router.put("/{blog_id}", response_model=BlogCreate, summary="Update a blog post")
async def update_blog(
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    blog_id: int,
    blog_update: BlogCreate,
):
    result = await blog_update_service(
        session=session,
        blog_id=blog_id,
        blog_update=blog_update,
        author_id=user.id,
    )
    return result


@router.delete("/{blog_id}", summary="Delete a blog post")
async def delete_blog(
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    blog_id: int,
):
    result = await blog_delete_service(
        session=session, blog_id=blog_id, author_id=user.id
    )
    return result
