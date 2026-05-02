from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from app.core.rbac import PERMISSION_DESCRIPTIONS
from app.dependencies.services import AuthServiceDep
from app.models.user import UserPublic

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    refreshUrl="/api/v1/auth/refresh",
    scopes=PERMISSION_DESCRIPTIONS,
)


async def get_current_user(
    security_scopes: SecurityScopes,
    auth_service: AuthServiceDep,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserPublic:
    user = await auth_service.get_user_by_access_token(
        access_token=token,
        required_scopes=list(security_scopes.scopes),
    )

    if user is None:
        authenticate_value = "Bearer"

        if security_scopes.scopes:
            authenticate_value = (
                f'Bearer scope="{security_scopes.scope_str}"'
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

    return user
