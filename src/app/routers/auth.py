from typing import Annotated

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
    Security,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

from app.core.rate_limit import limiter
from app.core.settings import settings
from app.dependencies.auth import get_current_user
from app.dependencies.services import AuthServiceDep
from app.models.user import UserPublic
from app.schemas.auth import (
    LogoutResponse,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)

router = APIRouter(prefix='/auth', tags=['Auth'])

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
    auth_service: AuthServiceDep,
):
    try:
        is_registered = await auth_service.register(data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    if not is_registered:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email already exists',
        )

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

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token is missing',
        )

    tokens = await auth_service.refresh_tokens(refresh_token)

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid refresh token',
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
