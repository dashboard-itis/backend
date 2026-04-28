from app.dependencies.repositories import RoleRepositoryDep, UserRepositoryDep
from app.models.user import UserCreate, UserPublic, UserUpdate
from app.schemas.user_filters import UserFilters
from app.utils.security import hash_password


class UserService:
    def __init__(
        self,
        user_repo: UserRepositoryDep,
        role_repo: RoleRepositoryDep,
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo

    async def get_all(self, filters: UserFilters) -> list[UserPublic]:
        db_filters = filters.model_dump(
            exclude={"skip", "limit", "search"},
            exclude_none=True,
        )

        users = await self.user_repo.fetch(
            skip=filters.skip,
            limit=filters.limit,
            filters=db_filters,
            search=filters.search,
        )
        return [UserPublic.model_validate(user) for user in users]

    async def get_by_id(self, user_id: int) -> UserPublic | None:
        user = await self.user_repo.get(user_id)
        return UserPublic.model_validate(user) if user else None

    async def get_by_email(self, email: str) -> UserPublic | None:
        user = await self.user_repo.get_by_email(email)
        return UserPublic.model_validate(user) if user else None

    async def create(self, user_data: UserCreate) -> UserPublic:
        existing = await self.get_by_email(user_data.email)

        if existing is not None:
            raise ValueError("Email already registered")

        create_data = user_data.model_dump(exclude={"password"})
        create_data["password_hash"] = hash_password(user_data.password)

        user = await self.user_repo.create(**create_data)
        return UserPublic.model_validate(user)

    async def update(self, user_id: int, user_data: UserUpdate) -> UserPublic | None:
        update_data = user_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password_hash"] = hash_password(update_data.pop("password"))

        user = await self.user_repo.update(user_id, **update_data)
        return UserPublic.model_validate(user) if user else None

    async def update_roles(
        self,
        user_id: int,
        role_names: list[str],
    ) -> UserPublic | None:
        user = await self.user_repo.get_with_roles(user_id)

        if user is None:
            return None

        roles = await self.role_repo.get_existing_by_names(role_names)

        if len(roles) != len(set(role_names)):
            existing_role_names = {role.name for role in roles}
            missing_roles = set(role_names) - existing_role_names
            raise ValueError(f"Roles not found: {', '.join(sorted(missing_roles))}")

        user.roles = roles
        updated_user = await self.user_repo.save(user)

        return UserPublic.model_validate(updated_user)

    async def delete(self, user_id: int) -> bool:
        user = await self.user_repo.delete(user_id)
        return user is not None
