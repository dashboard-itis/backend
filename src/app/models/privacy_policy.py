from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base
import enum


class RatingMode(str, enum.Enum):
    FULL = "full"  # Показывать ФИО
    ANONYMIZED = "anonymized"  # Показывать обезличенно


class PrivacyPolicy(Base):
    __tablename__ = "privacy_policies"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, unique=True)
    show_rating_to_students = Column(Boolean, nullable=False, default=True)
    rating_mode = Column(String, nullable=False, default=RatingMode.ANONYMIZED)
    allow_student_stats = Column(Boolean, nullable=False, default=True)
    version = Column(Integer, nullable=False, default=1)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    group = relationship("Group", back_populates="privacy_policy")