from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Stream(Base):
    __tablename__ = "streams"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    semester = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    group = relationship("Group", back_populates="streams")
    courses = relationship("Course", back_populates="stream")
    import_sources = relationship("ImportSource", back_populates="stream")