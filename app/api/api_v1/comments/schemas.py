from pydantic import BaseModel


class CommentSchema(BaseModel):
    id: int
    content: str
    author_id: int
    blog_id: int
