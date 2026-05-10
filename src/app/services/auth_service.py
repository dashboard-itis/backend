from datetime import datetime, timedelta, timezone
from secrets import randbelow
from typing import Annotated

from fastapi import BackgroundTasks, Depends

from app.core.auth import create_access_token, create_refresh_token, decode_jwt_token
from app.core.exceptions import (
    AccountNotConfirmedError,
    BadRequestError,
    ConflictError,
    InvalidConfirmationCodeError,
    NotFoundError,
    UnauthorizedError,
)
from app.core.settings import settings
from app.dependencies.repositories import (
    EmailNotificationRepositoryDep,
    RefreshSessionRepositoryDep,
    RoleRepositoryDep,
    UserRepositoryDep,
)
from app.models.email_notification import EmailNotification
from app.models.refresh_session import RefreshSession
from app.models.user import User, UserCreate, UserPublic
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.token import TokenData
from app.services.email_service import EmailService
from app.utils.security import hash_password, verify_password

ACCOUNT_CONFIRMATION_ACTION = 'account_confirmation'
PASSWORD_RESET_ACTION = 'password_reset'
EmailServiceDep = Annotated[EmailService, Depends(EmailService)]


class AuthService:
    def __init__(
        self,
        user_repo: UserRepositoryDep,
        role_repo: RoleRepositoryDep,
        refresh_session_repo: RefreshSessionRepositoryDep,
        email_notification_repo: EmailNotificationRepositoryDep,
        email_service: EmailServiceDep,
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.refresh_session_repo = refresh_session_repo
        self.email_notification_repo = email_notification_repo
        self.email_service = email_service

    async def register(
        self,
        data: RegisterRequest,
        background_tasks: BackgroundTasks,
    ) -> bool:
        existing_user = await self.user_repo.get_by_email(data.email)

        if existing_user is not None:
            raise ConflictError('User with this email already exists')

        user_create = UserCreate(**data.model_dump())

        user_data = user_create.model_dump(exclude={'password'})
        user_data['password_hash'] = hash_password(user_create.password)
        user_data['is_confirmed'] = False

        user = await self.user_repo.create(**user_data)

        public_role = await self.role_repo.get_by_name(settings.rbac.public_role)

        if public_role is None:
            raise BadRequestError('Public role does not exist')

        await self.user_repo.add_role(user, public_role)
        await self.send_account_confirmation(user, background_tasks)

        return True

    async def send_account_confirmation(
        self,
        user: User,
        background_tasks: BackgroundTasks,
    ) -> None:
        notification = await self.create_email_notification(
            user_id=user.id,
            action=ACCOUNT_CONFIRMATION_ACTION,
        )
        confirmation_url = (
            f'{settings.email.app_host}/api/v1/auth/confirm-account'
            f'?user_id={user.id}&code={notification.code}'
        )

        await self.email_service.send_template(
            background_tasks=background_tasks,
            subject='Confirm your Dashboard ITIS account',
            recipients=[user.email],
            template_name='account_confirmation.html',
            template_body={
                'first_name': user.first_name,
                'code': notification.code,
                'confirmation_url': confirmation_url,
            },
        )

    async def create_email_notification(
        self,
        user_id: int,
        action: str,
    ) -> EmailNotification:
        code = str(randbelow(900000) + 100000)
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.email.confirmation_code_lifetime_minutes,
        )
        return await self.email_notification_repo.create(
            user_id=user_id,
            action=action,
            code=code,
            expires_at=expires_at,
            is_used=False,
        )

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.user_repo.get_by_email_with_roles(email)

        if user is None:
            return None

        if not verify_password(password, user.password_hash):
            return None

        if not user.is_confirmed:
            raise AccountNotConfirmedError()

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
            raise NotFoundError('User not found')

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
            raise UnauthorizedError('Incorrect email or password')

        return await self.create_tokens_for_user(user)

    async def confirm_account(self, user_id: int, code: str) -> bool:
        notification = await self.email_notification_repo.get_active(
            user_id=user_id,
            action=ACCOUNT_CONFIRMATION_ACTION,
            code=code,
        )

        if notification is None:
            raise InvalidConfirmationCodeError()

        user = await self.user_repo.update(user_id, is_confirmed=True)

        if user is None:
            raise NotFoundError('User not found')

        await self.email_notification_repo.update(notification.id, is_used=True)

        return True

    async def request_password_reset(
        self,
        email: str,
        background_tasks: BackgroundTasks,
    ) -> bool:
        user = await self.user_repo.get_by_email(email)

        if user is None:
            return True

        notification = await self.create_email_notification(
            user_id=user.id,
            action=PASSWORD_RESET_ACTION,
        )

        await self.email_service.send_template(
            background_tasks=background_tasks,
            subject='Confirm Dashboard ITIS password change',
            recipients=[user.email],
            template_name='password_reset.html',
            template_body={
                'first_name': user.first_name,
                'code': notification.code,
            },
        )

        return True

    async def confirm_password_reset(
        self,
        user_id: int,
        code: str,
        password: str,
        password_confirm: str,
    ) -> bool:
        if password != password_confirm:
            raise BadRequestError('Passwords do not match')

        notification = await self.email_notification_repo.get_active(
            user_id=user_id,
            action=PASSWORD_RESET_ACTION,
            code=code,
        )

        if notification is None:
            raise InvalidConfirmationCodeError()

        user = await self.user_repo.update(
            user_id,
            password_hash=hash_password(password),
        )

        if user is None:
            raise NotFoundError('User not found')

        await self.email_notification_repo.update(notification.id, is_used=True)
        await self.invalidate_user_sessions(user_id)

        return True

    async def invalidate_user_sessions(self, user_id: int) -> None:
        sessions = await self.refresh_session_repo.fetch(
            filters={
                'user_id': user_id,
                'is_invalidated': False,
            },
            limit=1000,
        )

        for session in sessions:
            await self.refresh_session_repo.update(session.id, is_invalidated=True)

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
