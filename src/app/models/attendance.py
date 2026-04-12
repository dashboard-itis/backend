from __future__ import annotations

import enum
from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.user import User


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    EXCUSED = "excused"


class Attendance(BaseModel, table=True):
    __tablename__ = "attendance"

    course_id: int = Field(foreign_key="courses.id")
    student_id: int = Field(foreign_key="users.id")
    date: date
    status: AttendanceStatus = Field(default=AttendanceStatus.PRESENT)
    comment: str | None = None

    course: "Course | None" = Relationship(back_populates="attendance_records")
    student: "User | None" = Relationship(back_populates="attendance_records")