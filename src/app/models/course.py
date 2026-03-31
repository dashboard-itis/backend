from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("streams.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    stream = relationship("Stream", back_populates="courses")
    teacher = relationship("User", foreign_keys=[teacher_id], back_populates="taught_courses")
    assignments = relationship("Assignment", back_populates="course")
    attendance_records = relationship("Attendance", back_populates="course")
    import_sources = relationship("ImportSource", back_populates="course")