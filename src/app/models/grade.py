from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.user import User


class Grade(BaseModel, table=True):
    __tablename__ = "grades"

    assignment_id: int = Field(foreign_key="assignments.id")
    student_id: int = Field(foreign_key="users.id")
    score: float = Field(ge=0, le=100)
    comment: str | None = None

    assignment: "Assignment | None" = Relationship(back_populates="grades")
    student: "User | None" = Relationship(back_populates="grades")