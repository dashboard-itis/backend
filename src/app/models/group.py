from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BasePublicModel, BaseTableModel

if TYPE_CHECKING:
    from app.models.stream import Stream
    from app.models.user import User


class GroupBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    year: int | None = None
    stream_id: int | None = Field(default=None, foreign_key="streams.id")


class Group(GroupBase, BaseTableModel, table=True):
    __tablename__ = "groups"

    stream: "Stream | None" = Relationship(back_populates="groups")
    users: list["User"] = Relationship(back_populates="group")


class GroupCreate(GroupBase):
    pass


class GroupUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = None
    stream_id: int | None = None


class GroupPublic(GroupBase, BasePublicModel):
    pass


GroupCreate.model_rebuild()
GroupUpdate.model_rebuild()
GroupPublic.model_rebuild()