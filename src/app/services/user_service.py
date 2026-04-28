from app.dependencies.repositories import UserRepositoryDep
from app.models.user import UserCreate, UserPublic, UserUpdate
from app.schemas.user_filters import UserFilters
from app.utils.security import hash_password


class UserService:
    def __init__(self, repo: UserRepositoryDep):
        self.repo = repo

    async def get_all(self, filters: UserFilters) -> list[UserPublic]:
        db_filters = filters.model_dump(
            exclude={"skip", "limit", "search"},
            exclude_none=True,
        )

        users = await self.repo.get_all(
            skip=filters.skip,
            limit=filters.limit,
            filters=db_filters,
            search=filters.search,
        )
        return [UserPublic.model_validate(user) for user in users]

    async def get_by_id(self, user_id: int) -> UserPublic | None:
        user = await self.repo.get(user_id)
        return UserPublic.model_validate(user) if user else None

    async def get_by_email(self, email: str) -> UserPublic | None:
        users = await self.repo.get_all(filters={"email": email}, limit=1)
        if not users:
            return None
        return UserPublic.model_validate(users[0])

    async def create(self, user_data: UserCreate) -> UserPublic:
        existing = await self.get_by_email(user_data.email)
        if existing:
            raise ValueError("Email already registered")

        user = await self.repo.create(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role.value,
            group_id=user_data.group_id,
        )
        return UserPublic.model_validate(user)

    async def update(self, user_id: int, user_data: UserUpdate) -> UserPublic | None:
        update_data = user_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password_hash"] = hash_password(update_data.pop("password"))

        if "role" in update_data and update_data["role"] is not None:
            update_data["role"] = update_data["role"].value

        user = await self.repo.update(user_id, **update_data)
        return UserPublic.model_validate(user) if user else None

    async def delete(self, user_id: int) -> bool:
        deleted = await self.repo.delete(user_id)
        return deleted is not None