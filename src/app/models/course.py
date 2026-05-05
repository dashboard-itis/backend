from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.attendance import Attendance
    from app.models.stream import Stream
    from app.models.user import User


class CourseBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    stream_id: int | None = Field(default=None, foreign_key='streams.id')
    teacher_id: int | None = Field(default=None, foreign_key='users.id')


class Course(CourseBase, BaseModel, table=True):
    __tablename__ = 'courses'

    stream: Optional['Stream'] = Relationship(back_populates='courses')
    teacher: Optional['User'] = Relationship(back_populates='courses')
    assignments: list['Assignment'] = Relationship(back_populates='course')
    attendance_records: list['Attendance'] = Relationship(back_populates='course')


class CourseCreate(CourseBase):
    pass


class CourseUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    stream_id: int | None = None
    teacher_id: int | None = None


class CoursePublic(CourseBase, BaseModel):
    pass
