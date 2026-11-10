from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr = Field(max_length=150)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    image_url: str | None
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    username: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=150)
    image_url: str | None = Field(default=None, max_length=200)
