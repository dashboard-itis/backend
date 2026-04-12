from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.user import User


class SubmissionStatus(str, enum.Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    GRADED = "graded"


class Submission(BaseModel, table=True):
    __tablename__ = "submissions"

    assignment_id: int = Field(foreign_key="assignments.id")
    student_id: int = Field(foreign_key="users.id")
    content: str
    status: SubmissionStatus = Field(default=SubmissionStatus.PENDING)
    submitted_at: datetime | None = None

    assignment: "Assignment | None" = Relationship(back_populates="submissions")
    student: "User | None" = Relationship(back_populates="submissions")