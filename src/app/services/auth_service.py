from datetime import datetime, timezone

from app.core.auth import create_access_token, create_refresh_token, decode_jwt_token
from app.core.settings import settings
from app.dependencies.repositories import (
    RefreshSessionRepositoryDep,
    RoleRepositoryDep,
    UserRepositoryDep,
)
from app.models.refresh_session import RefreshSession
from app.models.user import User, UserCreate, UserPublic
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.token import TokenData
from app.utils.security import hash_password, verify_password


class AuthService:
    def __init__(
        self,
        user_repo: UserRepositoryDep,
        role_repo: RoleRepositoryDep,
        refresh_session_repo: RefreshSessionRepositoryDep,
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.refresh_session_repo = refresh_session_repo

    async def register(self, data: RegisterRequest) -> bool:
        existing_user = await self.user_repo.get_by_email(data.email)

        if existing_user is not None:
            return False

        user_create = UserCreate(**data.model_dump())

        user_data = user_create.model_dump(exclude={'password'})
        user_data['password_hash'] = hash_password(user_create.password)

        user = await self.user_repo.create(**user_data)

        public_role = await self.role_repo.get_by_name(settings.rbac.public_role)

        if public_role is None:
            raise ValueError('Public role does not exist')

        await self.user_repo.add_role(user, public_role)

        return True

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.user_repo.get_by_email_with_roles(email)

        if user is None:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    async def get_user_scopes(self, user: User) -> list[str]:
        scopes: set[str] = set()

        for role in user.roles:
            for permission in role.permissions:
                scopes.add(permission.scope)

        return sorted(scopes)

    async def create_tokens_for_user(self, user: User) -> TokenResponse:
        user_with_roles = await self.user_repo.get_by_id_with_roles(user.id)

        if user_with_roles is None:
            raise ValueError('User not found')

        scopes = await self.get_user_scopes(user_with_roles)

        access_token, access_data = create_access_token(
            user_id=user_with_roles.id,
            scopes=scopes,
        )

        refresh_token, refresh_data = create_refresh_token(
            user_id=user_with_roles.id,
            scopes=scopes,
        )

        refresh_session = RefreshSession(
            user_id=user_with_roles.id,
            access_token_jti=access_data.jti,
            refresh_token_jti=refresh_data.jti,
            expires_at=datetime.fromtimestamp(refresh_data.exp, tz=timezone.utc),
            is_invalidated=False,
        )

        await self.refresh_session_repo.save(refresh_session)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=access_data.exp,
            scope=access_data.scope,
        )

    async def login(self, email: str, password: str) -> TokenResponse | None:
        user = await self.authenticate_user(email, password)

        if user is None:
            return None

        return await self.create_tokens_for_user(user)

    async def get_user_by_access_token(
        self,
        access_token: str,
        required_scopes: list[str] | None = None,
    ) -> UserPublic | None:
        token_data = decode_jwt_token(access_token)

        if token_data is None:
            return None

        if required_scopes is not None:
            scopes_are_valid = self.validate_token_scopes(
                token_data=token_data,
                required_scopes=required_scopes,
            )

            if not scopes_are_valid:
                return None

        user = await self.user_repo.get(token_data.user_id)

        if user is None:
            return None

        return UserPublic.model_validate(user)

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse | None:
        token_data = decode_jwt_token(refresh_token)

        if token_data is None:
            return None

        refresh_sessions = await self.refresh_session_repo.fetch(
            filters={
                'user_id': token_data.user_id,
                'refresh_token_jti': token_data.jti,
                'is_invalidated': False,
            },
            limit=1,
        )

        if not refresh_sessions:
            return None

        refresh_session: RefreshSession = refresh_sessions[0]

        if not refresh_session.is_valid:
            return None

        await self.refresh_session_repo.update(
            refresh_session.id,
            is_invalidated=True,
        )

        user = await self.user_repo.get_by_id_with_roles(token_data.user_id)

        if user is None:
            return None

        return await self.create_tokens_for_user(user)

    async def logout(self, refresh_token: str) -> bool:
        token_data = decode_jwt_token(refresh_token)

        if token_data is None:
            return False

        refresh_sessions = await self.refresh_session_repo.fetch(
            filters={
                'user_id': token_data.user_id,
                'refresh_token_jti': token_data.jti,
                'is_invalidated': False,
            },
            limit=1,
        )

        if not refresh_sessions:
            return False

        refresh_session = refresh_sessions[0]

        await self.refresh_session_repo.update(
            refresh_session.id,
            is_invalidated=True,
        )

        return True

    def validate_token_scopes(
        self,
        token_data: TokenData,
        required_scopes: list[str],
    ) -> bool:
        if '*' in token_data.scopes:
            return True

        token_scopes = set(token_data.scopes)

        return all(required_scope in token_scopes for required_scope in required_scopes)
