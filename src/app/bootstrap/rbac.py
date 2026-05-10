from app.core.rbac import INITIAL_ROLE_SCOPES, PERMISSION_DESCRIPTIONS
from app.core.settings import settings
from app.models.permission import Permission
from app.models.role import Role
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.utils.rbac import split_scope
from app.utils.security import hash_password


class RBACBootstrapper:
    def __init__(
        self,
        user_repo: UserRepository,
        role_repo: RoleRepository,
        permission_repo: PermissionRepository,
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.permission_repo = permission_repo

    async def bootstrap(self) -> None:
        permissions = await self._create_permissions()
        roles = await self._create_roles()
        await self._assign_permissions_to_roles(roles, permissions)
        await self._create_admin_user(roles[settings.rbac.admin_role])

    async def _create_permissions(self) -> dict[str, Permission]:
        permissions: dict[str, Permission] = {}

        for scope, description in PERMISSION_DESCRIPTIONS.items():
            subject, action = split_scope(scope)

            permission = await self.permission_repo.get_or_create(
                subject=subject,
                action=action,
                description=description,
            )
            permissions[scope] = permission

        return permissions

    async def _create_roles(self) -> dict[str, Role]:
        roles: dict[str, Role] = {}

        for role_name in INITIAL_ROLE_SCOPES:
            role = await self.role_repo.get_or_create_by_name(role_name)
            roles[role_name] = role

        return roles

    async def _assign_permissions_to_roles(
        self,
        roles: dict[str, Role],
        permissions: dict[str, Permission],
    ) -> None:
        for role_name, scopes in INITIAL_ROLE_SCOPES.items():
            role = roles[role_name]

            if '*' in scopes:
                role.permissions = list(permissions.values())
            else:
                role.permissions = [
                    permissions[scope] for scope in scopes if scope in permissions
                ]

            await self.role_repo.save(role)

    async def _create_admin_user(self, admin_role: Role) -> None:
        admin = await self.user_repo.get_by_email(settings.admin.email)

        if admin is None:
            admin = await self.user_repo.create(
                email=settings.admin.email,
                first_name=settings.admin.first_name,
                last_name=settings.admin.last_name,
                password_hash=hash_password(settings.admin.password),
                is_confirmed=True,
            )
        elif not admin.is_confirmed:
            admin.is_confirmed = True

        admin.roles = [admin_role]
        await self.user_repo.save(admin)
