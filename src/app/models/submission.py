from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel


class SubmissionBase(SQLModel):
    assignment_id: int = Field(foreign_key="assignments.id")
    student_id: int = Field(foreign_key="users.id")
    content: str


class Submission(SubmissionBase, BaseModel, table=True):
    __tablename__ = "submissions"

    assignment: "Assignment | None" = Relationship(back_populates="submissions")
    student: "User | None" = Relationship(back_populates="submissions")


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(SQLModel):
    content: str | None = None


class SubmissionPublic(SubmissionBase, BaseModel):
    pass
