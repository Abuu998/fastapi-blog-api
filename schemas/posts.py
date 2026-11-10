from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from .users import UserResponse


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    user_id: str # TEMPORARY


class PostUpdate(PostBase):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    author: UserResponse
    created_at: datetime
    updated_at: datetime
