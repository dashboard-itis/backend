from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.user import User


class GradeBase(SQLModel):
    student_id: int = Field(foreign_key='users.id')
    course_id: int = Field(foreign_key='courses.id')
    score: float = Field(ge=0, le=100)
    comment: str | None = None


class Grade(GradeBase, BaseModel, table=True):
    __tablename__ = 'grades'

    student: Optional['User'] = Relationship(back_populates='grades')
    course: Optional['Course'] = Relationship(back_populates='grades')


class GradeCreate(GradeBase):
    pass


class GradeUpdate(SQLModel):
    student_id: int | None = None
    course_id: int | None = None
    score: float | None = Field(default=None, ge=0, le=100)
    comment: str | None = None


class GradePublic(GradeBase, BaseModel):
    pass
