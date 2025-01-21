from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.users.users import get_user_by_id


async def verify_user_exists(session: AsyncSession, user_id: int):

    try:
        await get_user_by_id(user_id=user_id, session=session)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )


def verify_ownership(resource_author_id: int, user_id: int):

    if resource_author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to modify this resource",
        )
