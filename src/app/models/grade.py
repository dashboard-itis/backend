from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.user import User


class GradeBase(SQLModel):
    value: int = Field(ge=0, le=100)
    student_id: int = Field(foreign_key="users.id")
    course_id: int = Field(foreign_key="courses.id")


class Grade(GradeBase, BaseModel, table=True):
    __tablename__ = "grades"

    student: "User | None" = Relationship(back_populates="grades")
    course: "Course | None" = Relationship(back_populates="grades")


class GradeCreate(GradeBase):
    pass


class GradeUpdate(SQLModel):
    value: int | None = Field(default=None, ge=0, le=100)
    student_id: int | None = None
    course_id: int | None = None


class GradePublic(GradeBase, BaseModel):
    pass
