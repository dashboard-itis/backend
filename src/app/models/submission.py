from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.user import User


class SubmissionBase(SQLModel):
    assignment_id: int = Field(foreign_key="assignments.id")
    student_id: int = Field(foreign_key="users.id")
    content: str


class Submission(SubmissionBase, BaseModel, table=True):
    __tablename__ = "submissions"

    assignment: Optional["Assignment"] = Relationship(back_populates="submissions")
    student: Optional["User"] = Relationship(back_populates="submissions")


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(SQLModel):
    content: str | None = None


class SubmissionPublic(SubmissionBase, BaseModel):
    pass
