from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.group import Group
    from app.models.import_source import ImportSource


class Stream(BaseModel, table=True):
    __tablename__ = "streams"

    group_id: int = Field(foreign_key="groups.id")
    semester: int = Field(ge=1, le=2)
    year: int = Field(ge=2000, le=2100)

    group: "Group | None" = Relationship(back_populates="streams")
    courses: list["Course"] = Relationship(back_populates="stream")
    import_sources: list["ImportSource"] = Relationship(back_populates="stream")