from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    year = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    users = relationship("User", back_populates="group")
    streams = relationship("Stream", back_populates="group")
    privacy_policy = relationship("PrivacyPolicy", back_populates="group", uselist=False)