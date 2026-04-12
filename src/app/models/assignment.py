from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.grade import Grade
    from app.models.submission import Submission


class Assignment(BaseModel, table=True):
    __tablename__ = "assignments"

    course_id: int = Field(foreign_key="courses.id")
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    max_score: float = Field(ge=0)
    weight: float | None = Field(default=None, ge=0, le=1)
    due_date: datetime | None = None

    course: "Course | None" = Relationship(back_populates="assignments")
    grades: list["Grade"] = Relationship(back_populates="assignment")
    submissions: list["Submission"] = Relationship(back_populates="assignment")