from __future__ import annotations

import enum
from datetime import date as dt_date
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.models.base import BaseTableModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.user import User


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    EXCUSED = "excused"


class AttendanceBase(SQLModel):
    course_id: int = Field(foreign_key="courses.id")
    student_id: int = Field(foreign_key="users.id")
    date: dt_date
    status: AttendanceStatus = Field(default=AttendanceStatus.PRESENT)
    comment: str | None = None


class Attendance(AttendanceBase, BaseTableModel, table=True):
    __tablename__ = "attendance"

    course: "Course | None" = Relationship(back_populates="attendance_records")
    student: "User | None" = Relationship(back_populates="attendance_records")


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(SQLModel):
    course_id: int | None = None
    student_id: int | None = None
    date: dt_date | None = None
    status: AttendanceStatus | None = None
    comment: str | None = None


class AttendancePublic(AttendanceBase, TimestampedModel):
    id: int