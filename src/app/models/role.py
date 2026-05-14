from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel
from app.models.links import RolePermissionLink, UserRoleLink

if TYPE_CHECKING:
    from app.models.permission import Permission
    from app.models.user import User


class RoleBase(SQLModel):
    name: str = Field(index=True, unique=True, min_length=1, max_length=50)
    description: str | None = None


class Role(RoleBase, BaseModel, table=True):
    __tablename__ = 'roles'

    users: list['User'] = Relationship(
        back_populates='roles',
        link_model=UserRoleLink,
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    permissions: list['Permission'] = Relationship(
        back_populates='roles',
        link_model=RolePermissionLink,
        sa_relationship_kwargs={'lazy': 'selectin'},
    )


class RoleCreate(RoleBase):
    pass


class RoleUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None


class RolePublic(RoleBase, BaseModel):
    pass
