from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BlogCreate(BaseModel):
    title: str
    content: str = Field(
        ...,
        max_length=1000,
        description="Content of the blog, must not exceed 1000 characters",
    )


class BlogRead(BlogCreate):
    id: int
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
