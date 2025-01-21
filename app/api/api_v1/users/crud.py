from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from api.api_v1.users.schemas import UserCreate, UserUpdate
from core.utils import hash_password
from db.models.users.user import User


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    users = select(User).order_by(User.id)
    result = await session.scalars(users)
    return result.all()


async def create_user_one(user_create: UserCreate, session: AsyncSession) -> User:

    existing_user_query = select(User).where(
        (User.email == user_create.email) | (User.username == user_create.username)
    )
    result = await session.execute(existing_user_query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        if existing_user.email == user_create.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )
        if existing_user.username == user_create.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists.",
            )

    hashed_password = hash_password(user_create.password)
    user_data = user_create.model_dump()
    user_data["password"] = hashed_password
    user = User(**user_data)
    # user = User(**user_create.model_dump())
    session.add(user)

    await session.commit()
    await session.refresh(user)
    return user


async def put_user_one(
    session: AsyncSession,
    user_id: int,
    user_update: UserUpdate,
) -> User:
    user = await get_user(user_id=user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.password = hash_password(user_update.password)

    session.add(user)
    await session.commit()
    await session.refresh(user)  #

    return user


async def user_delete_id(user_id: int, session: AsyncSession):
    user = await get_user(user_id=user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await session.delete(user)
    await session.commit()

    return {"message": f"User with ID {user_id} has been deleted."}


async def get_user(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


async def get_user_by_name(session: AsyncSession, name: str) -> User | None:
    stmt = select(User).where(User.username == name)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


async def get_user_by_email(session: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


async def search_users_by_username_or_email(
    session: AsyncSession, username: str, email: str
):
    query = select(User)
    if username is not None:
        query = get_user_by_name(session, username)
    if email is not None:
        query = get_user_by_email(session, email)

    result = await session.scalars(query)
    return result.all()


async def get_all_users_pag(
    session: AsyncSession, skip: int, limit: int
) -> Sequence[User]:
    query = select(User).offset(skip).limit(limit).order_by(User.id)
    result = await session.scalars(query)
    return result.all()


async def user_admin_update(session: AsyncSession, user_id: int):
    user = await get_user(user_id=user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user.is_admin = True
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"message": f"User with ID {user_id} has been updated and now admin."}
