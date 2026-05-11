from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Cookie,
    Depends,
    Request,
    Response,
    Security,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

from app.core.error_responses import AUTH_ERROR_RESPONSES
from app.core.exceptions import UnauthorizedError
from app.core.rate_limit import limiter
from app.core.settings import settings
from app.dependencies.auth import get_current_user
from app.dependencies.services import AuthServiceDep
from app.models.user import UserPublic
from app.schemas.auth import (
    ConfirmAccountRequest,
    LogoutResponse,
    MessageResponse,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    responses=AUTH_ERROR_RESPONSES,
)

REFRESH_TOKEN_COOKIE_NAME = 'refresh_token'

RefreshTokenCookie = Annotated[
    str | None,
    Cookie(alias=REFRESH_TOKEN_COOKIE_NAME),
]


@router.post(
    '/register',
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(settings.rate_limit.auth_limit)
async def register(
    request: Request,  # noqa: ARG001
    data: RegisterRequest,
    background_tasks: BackgroundTasks,
    auth_service: AuthServiceDep,
):
    await auth_service.register(data, background_tasks)

    return RegisterResponse(success=True)


@router.post('/login', response_model=TokenResponse)
@limiter.limit(settings.rate_limit.auth_limit)
async def login(
    request: Request,  # noqa: ARG001
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
):
    tokens = await auth_service.login(
        email=form_data.username,
        password=form_data.password,
    )

    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=tokens.refresh_token,
        max_age=int(settings.auth.refresh_token_lifetime.total_seconds()),
        httponly=True,
        secure=False,
        samesite='lax',
    )

    return tokens


@router.get('/me', response_model=UserPublic)
async def me(
    current_user: Annotated[
        UserPublic,
        Security(get_current_user, scopes=['auth:me']),
    ],
):
    return current_user


@router.post('/refresh', response_model=TokenResponse)
@limiter.limit(settings.rate_limit.auth_limit)
async def refresh(
    request: Request,  # noqa: ARG001
    response: Response,
    auth_service: AuthServiceDep,
    refresh_token: RefreshTokenCookie = None,
):
    if refresh_token is None:
        raise UnauthorizedError('Refresh token is missing')

    tokens = await auth_service.refresh_tokens(refresh_token)

    if tokens is None:
        raise UnauthorizedError('Invalid refresh token')

    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=tokens.refresh_token,
        max_age=int(settings.auth.refresh_token_lifetime.total_seconds()),
        httponly=True,
        secure=False,
        samesite='lax',
    )

    return tokens


@router.post('/confirm-account', response_model=MessageResponse)
async def confirm_account(
    data: ConfirmAccountRequest,
    auth_service: AuthServiceDep,
):
    await auth_service.confirm_account(user_id=data.user_id, code=data.code)
    return MessageResponse(success=True, message='Account confirmed')


@router.post('/password-reset/request', response_model=MessageResponse)
@limiter.limit(settings.rate_limit.auth_limit)
async def request_password_reset(
    request: Request,  # noqa: ARG001
    data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    auth_service: AuthServiceDep,
):
    await auth_service.request_password_reset(
        email=str(data.email),
        background_tasks=background_tasks,
    )
    return MessageResponse(
        success=True,
        message='If the email exists, confirmation code was sent',
    )


@router.post('/password-reset/confirm', response_model=MessageResponse)
@limiter.limit(settings.rate_limit.auth_limit)
async def confirm_password_reset(
    request: Request,  # noqa: ARG001
    data: PasswordResetConfirmRequest,
    auth_service: AuthServiceDep,
):
    await auth_service.confirm_password_reset(
        user_id=data.user_id,
        code=data.code,
        password=data.password,
        password_confirm=data.password_confirm,
    )
    return MessageResponse(success=True, message='Password changed')


@router.post('/logout', response_model=LogoutResponse)
async def logout(
    response: Response,
    auth_service: AuthServiceDep,
    refresh_token: RefreshTokenCookie = None,
):
    if refresh_token is not None:
        await auth_service.logout(refresh_token)

    response.delete_cookie(key=REFRESH_TOKEN_COOKIE_NAME)

    return LogoutResponse(success=True)
