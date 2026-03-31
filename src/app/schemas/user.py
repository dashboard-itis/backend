from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    CURATOR = "curator"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)

class UserCreate(UserBase):
    password: str = Field(min_length=8)
    role: UserRole = UserRole.STUDENT
    group_id: Optional[int] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[UserRole] = None
    group_id: Optional[int] = None

class UserPublic(UserBase):
    id: int
    role: UserRole
    group_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True