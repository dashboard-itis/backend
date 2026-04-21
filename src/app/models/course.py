from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.models.base import BaseTableModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.attendance import Attendance
    from app.models.import_source import ImportSource
    from app.models.stream import Stream
    from app.models.user import User


class CourseBase(SQLModel):
    name: str = Field(min_length=1, max_length=150)
    stream_id: int = Field(foreign_key="streams.id")
    teacher_id: int = Field(foreign_key="users.id")
    description: str | None = None


class Course(CourseBase, BaseTableModel, table=True):
    __tablename__ = "courses"

    stream: "Stream | None" = Relationship(back_populates="courses")
    teacher: "User | None" = Relationship(back_populates="taught_courses")
    assignments: list["Assignment"] = Relationship(back_populates="course")
    attendance_records: list["Attendance"] = Relationship(back_populates="course")
    import_sources: list["ImportSource"] = Relationship(back_populates="course")


class CourseCreate(CourseBase):
    pass


class CourseUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    stream_id: int | None = None
    teacher_id: int | None = None
    description: str | None = None


class CoursePublic(CourseBase, TimestampedModel):
    id: int