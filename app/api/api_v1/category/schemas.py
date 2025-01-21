from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str
    model_path: str = Field(
        ...,
        description="The path to the model associated with the category. For example, 'app.db.models.comments.Comment'.",
        examples=["app.db.models.comments.Comment"],
    )


class CategoryRead(BaseModel):
    id: int
    name: str
    model_path: str

    class Config:
        from_attributes = True
