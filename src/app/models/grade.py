from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.models.base import BaseTableModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.user import User


class GradeBase(SQLModel):
    assignment_id: int = Field(foreign_key="assignments.id")
    student_id: int = Field(foreign_key="users.id")
    score: float = Field(ge=0, le=100)
    comment: str | None = None


class Grade(GradeBase, BaseTableModel, table=True):
    __tablename__ = "grades"

    assignment: "Assignment | None" = Relationship(back_populates="grades")
    student: "User | None" = Relationship(back_populates="grades")


class GradeCreate(GradeBase):
    pass


class GradeUpdate(SQLModel):
    assignment_id: int | None = None
    student_id: int | None = None
    score: float | None = Field(default=None, ge=0, le=100)
    comment: str | None = None


class GradePublic(GradeBase, TimestampedModel):
    id: int