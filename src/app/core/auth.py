from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from jwt import InvalidTokenError

from app.core.settings import settings
from app.schemas.token import TokenData


def create_jwt_token(
    user_id: int,
    lifetime: timedelta,
    scopes: list[str],
) -> tuple[str, TokenData]:
    now = datetime.now(timezone.utc)
    expires_at = now + lifetime

    token_data = TokenData(
        sub=str(user_id),
        iat=int(now.timestamp()),
        exp=int(expires_at.timestamp()),
        jti=str(uuid4()),
        scope=' '.join(scopes),
    )

    token = jwt.encode(
        token_data.model_dump(),
        settings.auth.secret_key,
        algorithm=settings.auth.algorithm,
    )

    return token, token_data


def create_access_token(user_id: int, scopes: list[str]) -> tuple[str, TokenData]:
    return create_jwt_token(
        user_id=user_id,
        lifetime=settings.auth.access_token_lifetime,
        scopes=scopes,
    )


def create_refresh_token(user_id: int, scopes: list[str]) -> tuple[str, TokenData]:
    return create_jwt_token(
        user_id=user_id,
        lifetime=settings.auth.refresh_token_lifetime,
        scopes=scopes,
    )


def decode_jwt_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(
            token,
            settings.auth.secret_key,
            algorithms=[settings.auth.algorithm],
        )
        return TokenData.model_validate(payload)
    except (InvalidTokenError, ValueError):
        return None
