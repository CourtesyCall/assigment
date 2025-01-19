from pydantic import BaseModel


class LikeBase(BaseModel):
    user_id: int
    category_id: int
    target_id: int

    class Config:
        from_attributes = True


class LikeCreate(LikeBase):
    pass


class LikeRead(LikeBase):
    id: int
