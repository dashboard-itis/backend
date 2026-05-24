from sqlalchemy.orm import selectinload
from sqlmodel import delete, select

from app.dependencies.session import SessionDep
from app.models.email_notification import EmailNotification
from app.models.links import UserRoleLink
from app.models.refresh_session import RefreshSession
from app.models.role import Role
from app.models.user import User
from app.repositories.base import Repository


class UserRepository(Repository[User]):
    def __init__(self, session: SessionDep):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.exec(
            select(User).where(User.email == email).options(selectinload(User.roles))
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
            select(User).where(User.id == user_id).options(selectinload(User.roles))
        )
        return result.first()

    async def fetch_with_roles(
        self,
        filters: dict | None = None,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
    ) -> list[User]:
        query = select(User).options(selectinload(User.roles))
        query = self._apply_filters(query, filters=filters, search=search)
        query = query.offset(skip).limit(limit)

        result = await self.session.exec(query)
        return list(result.all())

    async def add_role(self, user: User, role: Role) -> User:
        if all(existing_role.id != role.id for existing_role in user.roles):
            user.roles.append(role)

        return await self.save(user)

    async def update_roles(self, user: User, roles: list[Role]) -> User:
        user.roles = roles
        return await self.save(user)

    async def delete(self, object_id: int) -> User | None:
        user = await self.get(object_id)

        if user is None:
            return None

        await self.session.exec(
            delete(EmailNotification).where(EmailNotification.user_id == object_id)
        )
        await self.session.exec(
            delete(RefreshSession).where(RefreshSession.user_id == object_id)
        )
        await self.session.exec(
            delete(UserRoleLink).where(UserRoleLink.user_id == object_id)
        )
        await self.session.delete(user)
        await self.session.commit()

        return user
