from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.models.base import BaseTableModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.group import Group
    from app.models.import_source import ImportSource


class StreamBase(SQLModel):
    group_id: int = Field(foreign_key="groups.id")
    semester: int = Field(ge=1, le=2)
    year: int = Field(ge=2000, le=2100)


class Stream(StreamBase, BaseTableModel, table=True):
    __tablename__ = "streams"

    group: "Group | None" = Relationship(back_populates="streams")
    courses: list["Course"] = Relationship(back_populates="stream")
    import_sources: list["ImportSource"] = Relationship(back_populates="stream")


class StreamCreate(StreamBase):
    pass


class StreamUpdate(SQLModel):
    group_id: int | None = None
    semester: int | None = Field(default=None, ge=1, le=2)
    year: int | None = Field(default=None, ge=2000, le=2100)


class StreamPublic(StreamBase, TimestampedModel):
    id: int