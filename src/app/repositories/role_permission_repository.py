from app.dependencies.session import SessionDep
from app.models.permission import Permission
from app.models.role import Role
from app.repositories.base import Repository


class RolePermissionRepository(Repository[Role]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Role)

    async def update_permissions(
        self,
        role: Role,
        permissions: list[Permission],
    ) -> Role:
        role.permissions = permissions
        return await self.save(role)
