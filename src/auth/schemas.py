from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.books.schemas import BookMinResponse


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=20)


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_verified: bool
    books: List = [BookMinResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserRegisterResponse(BaseModel):
    message: str
    user: UserResponse


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=20)
