from typing import Annotated, Optional
from fastapi import HTTPException, status
from annotated_types import MaxLen, MinLen
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: Annotated[str, MinLen(3), MaxLen(15)]
    email: EmailStr
    password: Annotated[str, MinLen(8)]


class UserCreate(UserSchema):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] | None = Field(None, min_length=3, max_length=15)
    email: Optional[EmailStr] | None = None
    password: Optional[str] | None = Field(None, min_length=8)

    @model_validator(mode="before")
    def normalize_empty_fields(cls, values):
        return {key: value if value != "" else None for key, value in values.items()}

    @model_validator(mode="after")
    def check_at_least_one_field(cls, values):
        if not any(values.dict().values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided.",
            )
        return values


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    active: bool = True

    model_config = ConfigDict(from_attributes=True)
