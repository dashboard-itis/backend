from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.dependencies.session import SessionDep
from app.models.role import Role
from app.repositories.base import Repository


class RoleRepository(Repository[Role]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Role)

    async def get_by_name(self, name: str) -> Role | None:
        result = await self.session.exec(
            select(Role)
            .where(Role.name == name)
            .options(selectinload(Role.permissions))
        )
        return result.first()

    async def get_by_names(self, role_names: list[str]) -> list[Role]:
        if not role_names:
            return []

        result = await self.session.exec(
            select(Role)
            .where(Role.name.in_(role_names))
            .options(selectinload(Role.permissions))
        )
        return list(result.all())

    async def get_or_create_by_name(self, name: str) -> Role:
        role = await self.get_by_name(name)

        if role is None:
            role = await self.create(name=name)

        return role
