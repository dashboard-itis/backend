from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base
import enum


class UserRole(str, enum.Enum):
    STUDENT = "student"
    CURATOR = "curator"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    group = relationship("Group", back_populates="users")
    grades = relationship("Grade", back_populates="student")
    submissions = relationship("Submission", back_populates="student")
    attendance_records = relationship("Attendance", back_populates="student")
    taught_courses = relationship("Course", foreign_keys="Course.teacher_id", back_populates="teacher")