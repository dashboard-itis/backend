from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.dependencies.session import SessionDep
from app.models.role import Role
from app.models.user import User
from app.repositories.base import Repository


class UserRepository(Repository[User]):
    def __init__(self, session: SessionDep):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.exec(
            select(User)
            .where(User.email == email)
            .options(selectinload(User.roles))
        )
        return result.first()

    async def get_by_email_with_roles(self, email: str) -> User | None:
        result = await self.session.exec(
            select(User)
            .where(User.email == email)
            .options(selectinload(User.roles).selectinload(Role.permissions))
        )
        return result.first()

    async def get_by_id_with_roles(self, user_id: int) -> User | None:
        result = await self.session.exec(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.roles).selectinload(Role.permissions))
        )
        return result.first()

    async def get_with_roles(self, user_id: int) -> User | None:
        result = await self.session.exec(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.roles))
        )
        return result.first()

    async def add_role(self, user: User, role: Role) -> User:
        if all(existing_role.id != role.id for existing_role in user.roles):
            user.roles.append(role)

        return await self.save(user)

    async def update_roles(self, user: User, roles: list[Role]) -> User:
        user.roles = roles
        return await self.save(user)
