from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base
import enum


class ImportStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImportSource(Base):
    __tablename__ = "import_sources"

    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("streams.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    file_name = Column(String, nullable=False)
    uploaded_by = Column(String, nullable=False)
    status = Column(String, nullable=False, default=ImportStatus.PENDING)
    error_message = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    processed_at = Column(DateTime, nullable=True)

    stream = relationship("Stream", back_populates="import_sources")
    course = relationship("Course", back_populates="import_sources")