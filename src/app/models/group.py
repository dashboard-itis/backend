from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.privacy_policy import PrivacyPolicy
    from app.models.stream import Stream
    from app.models.user import User


class GroupBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    year: int | None = None


class Group(GroupBase, BaseModel, table=True):
    __tablename__ = "groups"

    users: list["User"] = Relationship(back_populates="group")
    streams: list["Stream"] = Relationship(back_populates="group")
    privacy_policy: Optional["PrivacyPolicy"] = Relationship(back_populates="group")


class GroupCreate(GroupBase):
    pass


class GroupUpdate(SQLModel):
    name: str | None = None
    year: int | None = None


class GroupPublic(GroupBase, BaseModel):
    pass
