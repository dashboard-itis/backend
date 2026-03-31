from app.dependencies.session import SessionDep
from app.utils.repository import Repository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserPublic
from app.utils.security import hash_password
from typing import Optional


class UserService:
    def __init__(self, db: SessionDep):
        self.db = db
        self.repo = Repository[User](db, User)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        email: Optional[str] = None,
        role: Optional[str] = None,
        group_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> list[UserPublic]:

        filters = {}
        if email:
            filters["email"] = email
        if role:
            filters["role"] = role
        if group_id:
            filters["group_id"] = group_id

        users = await self.repo.get_all(
            skip=skip,
            limit=limit,
            filters=filters,
            search=search
        )

        return [UserPublic.model_validate(u) for u in users]

    async def get_by_id(self, user_id: int) -> Optional[UserPublic]:
        user = await self.repo.get(user_id)
        return UserPublic.model_validate(user) if user else None

    async def get_by_email(self, email: str) -> Optional[UserPublic]:
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
            group_id=user_data.group_id
        )

        return UserPublic.model_validate(user)

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserPublic]:
        update_data = user_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password_hash"] = hash_password(update_data.pop("password"))

        user = await self.repo.update(user_id, **update_data)
        return UserPublic.model_validate(user) if user else None

    async def delete(self, user_id: int) -> bool:
        user = await self.repo.delete(user_id)
        return user is not None