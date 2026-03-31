from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    EXCUSED = "excused"
    LATE = "late"


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False, default=AttendanceStatus.PRESENT)
    comment = Column(String, nullable=True)

    course = relationship("Course", back_populates="attendance_records")
    student = relationship("User", back_populates="attendance_records")