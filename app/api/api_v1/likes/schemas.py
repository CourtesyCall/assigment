from pydantic import BaseModel

from api.api_v1.category.schemas import CategoryRead
from api.api_v1.users.schemas import UserSchema


class LikeBase(BaseModel):
    category_id: int
    target_id: int

    class Config:
        from_attributes = True


# class LikeInfo(BaseModel):
#     like_id: int
#     target_id: int
#     category: CategoryRead
#     user: UserSchema


class LikeCreate(LikeBase):
    pass


class LikeRead(LikeBase):
    id: int
