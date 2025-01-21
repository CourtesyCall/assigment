from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.blogs.schemas import BlogCreate
from api.api_v1.users.users import get_user_by_id
from core.error_handler import verify_user_exists, verify_ownership
from db.models.blogs.blog import Blog


async def blog_create_service(session: AsyncSession, blog: BlogCreate, author_id: int):
    await verify_user_exists(session, author_id)
    if blog.title:
        blog.title = blog.title.strip()
    if blog.content:
        blog.content = blog.content.strip()
    blog_create = Blog(title=blog.title, content=blog.content, author_id=author_id)
    session.add(blog_create)
    await session.commit()
    await session.refresh(blog_create)
    return blog_create


async def get_all_blogs(session: AsyncSession) -> Sequence[Blog]:
    blogs = select(Blog).order_by(Blog.id)
    result = await session.scalars(blogs)
    return result.all()


async def blog_update_service(
    session: AsyncSession, blog_id: int, blog_update: BlogCreate, author_id: int
):
    await verify_user_exists(session, author_id)

    blog = await session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized or not found"
        )
    await verify_ownership(blog.author_id, author_id, session)
    if blog_update.title:
        blog_update.title = blog_update.title.strip()
    if blog_update.content:
        blog_update.content = blog_update.content.strip()

    for key, value in blog_update.model_dump(exclude_unset=True).items():
        setattr(blog, key, value)
    session.add(blog)
    await session.commit()
    await session.refresh(blog)
    return blog


async def blog_delete_service(session: AsyncSession, blog_id: int, author_id: int):
    await verify_user_exists(session, author_id)

    blog = await session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized or not found"
        )
    await verify_ownership(blog.author_id, author_id, session)
    await session.delete(blog)
    await session.commit()
    return {"message": "Blog deleted"}
