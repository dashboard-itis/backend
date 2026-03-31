from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    assignment = relationship("Assignment", back_populates="grades")
    student = relationship("User", back_populates="grades")