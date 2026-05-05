from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel
from app.models.links import RolePermissionLink

if TYPE_CHECKING:
    from app.models.role import Role


class PermissionBase(SQLModel):
    subject: str = Field(index=True, min_length=1, max_length=100)
    action: str = Field(index=True, min_length=1, max_length=100)
    description: str | None = None

    @property
    def scope(self) -> str:
        return f'{self.subject}:{self.action}'


class Permission(PermissionBase, BaseModel, table=True):
    __tablename__ = 'permissions'
    __table_args__ = (
        UniqueConstraint('subject', 'action', name='uq_permissions_subject_action'),
    )

    roles: list['Role'] = Relationship(
        back_populates='permissions',
        link_model=RolePermissionLink,
    )


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(SQLModel):
    subject: str | None = Field(default=None, min_length=1, max_length=100)
    action: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class PermissionPublic(PermissionBase, BaseModel):
    pass
