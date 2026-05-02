
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.group import Group


class PrivacyPolicyBase(SQLModel):
    group_id: int = Field(foreign_key="groups.id", unique=True)
    show_rating_to_students: bool = True
    rating_mode: str = "anonymized"
    allow_student_stats: bool = True
    version: int = Field(default=1, ge=1)


class PrivacyPolicy(PrivacyPolicyBase, BaseModel, table=True):
    __tablename__ = "privacy_policies"

    group: Optional["Group"] = Relationship(back_populates="privacy_policy")


class PrivacyPolicyCreate(PrivacyPolicyBase):
    pass


class PrivacyPolicyUpdate(SQLModel):
    show_rating_to_students: bool | None = None
    rating_mode: str | None = None
    allow_student_stats: bool | None = None
    version: int | None = Field(default=None, ge=1)


class PrivacyPolicyPublic(PrivacyPolicyBase, BaseModel):
    pass
