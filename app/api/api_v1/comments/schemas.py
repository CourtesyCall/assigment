from pydantic import BaseModel, Field


class CommentSchema(BaseModel):
    content: str = Field(
        ...,
        max_length=1000,
        description="Content of the comment, must not exceed 1000 characters",
    )
    author_id: int
    blog_id: int


class CommentUpdate(BaseModel):
    id: int
    content: str = Field(
        ...,
        max_length=1000,
        description="Content of the comment, must not exceed 1000 characters",
    )


class CommentsRead(CommentSchema):
    id: int
