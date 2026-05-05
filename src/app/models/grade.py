from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.user import User


class GradeBase(SQLModel):
    student_id: int = Field(foreign_key='users.id')
    assignment_id: int = Field(foreign_key='assignments.id')
    score: float = Field(ge=0, le=100)
    comment: str | None = None


class Grade(GradeBase, BaseModel, table=True):
    __tablename__ = 'grades'

    student: Optional['User'] = Relationship(back_populates='grades')
    assignment: Optional['Assignment'] = Relationship(back_populates='grades')


class GradeCreate(GradeBase):
    pass


class GradeUpdate(SQLModel):
    student_id: int | None = None
    assignment_id: int | None = None
    score: float | None = Field(default=None, ge=0, le=100)
    comment: str | None = None


class GradePublic(GradeBase, BaseModel):
    pass
