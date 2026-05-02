from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.grade import Grade
    from app.models.submission import Submission


class AssignmentBase(SQLModel):
    course_id: int = Field(foreign_key="courses.id")
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    max_score: float = Field(ge=0)
    weight: float | None = Field(default=None, ge=0, le=1)
    due_date: datetime | None = None


class Assignment(AssignmentBase, BaseModel, table=True):
    __tablename__ = "assignments"

    course: Optional["Course"] = Relationship(back_populates="assignments")
    grades: list["Grade"] = Relationship(back_populates="assignment")
    submissions: list["Submission"] = Relationship(back_populates="assignment")


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(SQLModel):
    course_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    max_score: float | None = Field(default=None, ge=0)
    weight: float | None = Field(default=None, ge=0, le=1)
    due_date: datetime | None = None


class AssignmentPublic(AssignmentBase, BaseModel):
    pass
