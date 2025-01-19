from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BlogCreate(BaseModel):
    title: str
    content: str


class BlogRead(BlogCreate):
    id: int
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
