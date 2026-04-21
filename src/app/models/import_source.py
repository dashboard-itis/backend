from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.models.base import BaseTableModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.stream import Stream


class ImportStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImportSourceBase(SQLModel):
    stream_id: int = Field(foreign_key="streams.id")
    course_id: int = Field(foreign_key="courses.id")
    file_name: str = Field(min_length=1, max_length=255)
    uploaded_by: str = Field(min_length=1, max_length=255)
    status: ImportStatus = Field(default=ImportStatus.PENDING)


class ImportSource(ImportSourceBase, BaseTableModel, table=True):
    __tablename__ = "import_sources"

    stream: "Stream | None" = Relationship(back_populates="import_sources")
    course: "Course | None" = Relationship(back_populates="import_sources")


class ImportSourceCreate(ImportSourceBase):
    pass


class ImportSourceUpdate(SQLModel):
    stream_id: int | None = None
    course_id: int | None = None
    file_name: str | None = Field(default=None, min_length=1, max_length=255)
    uploaded_by: str | None = Field(default=None, min_length=1, max_length=255)
    status: ImportStatus | None = None


class ImportSourcePublic(ImportSourceBase, TimestampedModel):
    id: int