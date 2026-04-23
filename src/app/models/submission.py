from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IdModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.user import User


class SubmissionStatus(str, enum.Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    GRADED = "graded"


class SubmissionBase(SQLModel):
    assignment_id: int = Field(foreign_key="assignments.id")
    student_id: int = Field(foreign_key="users.id")
    content: str


class Submission(SubmissionBase, IdModel, TimestampedModel, table=True):
    __tablename__ = "submissions"

    status: SubmissionStatus = Field(default=SubmissionStatus.PENDING)
    submitted_at: datetime | None = None

    assignment: "Assignment | None" = Relationship(back_populates="submissions")
    student: "User | None" = Relationship(back_populates="submissions")


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(SQLModel):
    content: str | None = None
    status: SubmissionStatus | None = None
    submitted_at: datetime | None = None


class SubmissionPublic(SubmissionBase):
    id: int
    status: SubmissionStatus
    submitted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime