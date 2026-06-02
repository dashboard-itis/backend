from typing import TypedDict

from fastapi import Request

from app.core.exceptions import UnauthorizedError
from app.dependencies.services import AuthServiceDep, CourseServiceDep
from app.models.user import UserPublic
from app.services.auth_service import AuthService
from app.services.course_service import CourseService


class GraphQLContext(TypedDict):
    request: Request
    auth_service: AuthService
    course_service: CourseService


async def get_context(
    request: Request,
    auth_service: AuthServiceDep,
    course_service: CourseServiceDep,
) -> GraphQLContext:
    return {
        'request': request,
        'auth_service': auth_service,
        'course_service': course_service,
    }


async def require_current_user(
    context: GraphQLContext,
    scopes: list[str],
) -> UserPublic:
    authorization = context['request'].headers.get('Authorization')

    if authorization is None:
        raise UnauthorizedError('Missing Authorization header')

    scheme, _, token = authorization.partition(' ')

    if scheme.lower() != 'bearer' or not token:
        raise UnauthorizedError('Invalid Authorization header')

    user = await context['auth_service'].get_user_by_access_token(
        access_token=token,
        required_scopes=scopes,
    )

    if user is None:
        raise UnauthorizedError('Invalid token or not enough permissions')

    return user
