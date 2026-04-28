from sqlmodel import Field, SQLModel


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_role_links"

    user_id: int | None = Field(
        default=None,
        foreign_key="users.id",
        primary_key=True,
    )
    role_id: int | None = Field(
        default=None,
        foreign_key="roles.id",
        primary_key=True,
    )


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = "role_permission_links"

    role_id: int | None = Field(
        default=None,
        foreign_key="roles.id",
        primary_key=True,
    )
    permission_id: int | None = Field(
        default=None,
        foreign_key="permissions.id",
        primary_key=True,
    )
