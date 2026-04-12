from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

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


class User(BaseModel, table=True):
    __tablename__ = "users"

    email: str = Field(index=True, unique=True, min_length=5, max_length=255)
    password_hash: str
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    role: UserRole = Field(default=UserRole.STUDENT)
    group_id: int | None = Field(default=None, foreign_key="groups.id")

    group: "Group | None" = Relationship(back_populates="users")
    grades: list["Grade"] = Relationship(back_populates="student")
    submissions: list["Submission"] = Relationship(back_populates="student")
    attendance_records: list["Attendance"] = Relationship(back_populates="student")
    taught_courses: list["Course"] = Relationship(back_populates="teacher")