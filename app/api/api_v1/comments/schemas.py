from pydantic import BaseModel


class CommentSchema(BaseModel):
    content: str
    author_id: int
    blog_id: int


class CommentsRead(CommentSchema):
    id: int
