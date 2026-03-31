from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base
import enum


class SubmissionStatus(str, enum.Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    GRADED = "graded"
    LATE = "late"


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=True)
    status = Column(String, nullable=False, default=SubmissionStatus.PENDING)
    submitted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("User", back_populates="submissions")