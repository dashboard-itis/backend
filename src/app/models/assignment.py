from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    max_score = Column(Float, nullable=False)
    weight = Column(Float, nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    course = relationship("Course", back_populates="assignments")
    grades = relationship("Grade", back_populates="assignment")
    submissions = relationship("Submission", back_populates="assignment")