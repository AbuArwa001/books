from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=20)


class UserResponse(BaseModel):
    uid: str
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_verified: bool
    created_at: str
    updated_at: str