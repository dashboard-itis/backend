from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IdModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.attendance import Attendance
    from app.models.course import Course
    from app.models.grade import Grade
    from app.models.group import Group
    from app.models.submission import Submission


class UserRole(str, enum.Enum):
    STUDENT = "student"
    CURATOR = "curator"
    ADMIN = "admin"


class UserBase(SQLModel):
    email: EmailStr = Field(max_length=255)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)


class User(UserBase, IdModel, TimestampedModel, table=True):
    __tablename__ = "users"

    password_hash: str
    role: UserRole = Field(default=UserRole.STUDENT)
    group_id: int | None = Field(default=None, foreign_key="groups.id")

    group: "Group | None" = Relationship(back_populates="users")
    grades: list["Grade"] = Relationship(back_populates="student")
    submissions: list["Submission"] = Relationship(back_populates="student")
    attendance_records: list["Attendance"] = Relationship(back_populates="student")
    taught_courses: list["Course"] = Relationship(back_populates="teacher")


class UserCreate(UserBase):
    password: str = Field(min_length=8)
    role: UserRole = Field(default=UserRole.STUDENT)
    group_id: int | None = None


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    password: str | None = Field(default=None, min_length=8)
    role: UserRole | None = None
    group_id: int | None = None


class UserPublic(UserBase):
    id: int
    role: UserRole
    group_id: int | None = None
    created_at: datetime
    updated_at: datetime