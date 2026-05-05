from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import UserServiceDep
from app.models.user import UserCreate, UserPublic, UserUpdate
from app.schemas.user_filters import UserFilters
from app.schemas.user_roles import UserRolesUpdate

router = APIRouter(prefix='/users', tags=['Users'])

UserFiltersDep = Annotated[UserFilters, Depends()]


@router.get(
    '/',
    response_model=list[UserPublic],
    dependencies=[Security(get_current_user, scopes=['users:list'])],
)
async def get_users(
    service: UserServiceDep,
    filters: UserFiltersDep,
):
    return await service.get_all(filters)


@router.get(
    '/{user_id}',
    response_model=UserPublic,
    dependencies=[Security(get_current_user, scopes=['users:read'])],
)
async def get_user(user_id: int, service: UserServiceDep):
    user = await service.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    return user


@router.post(
    '/',
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['users:create'])],
)
async def create_user(user_data: UserCreate, service: UserServiceDep):
    try:
        return await service.create(user_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    '/{user_id}',
    response_model=UserPublic,
    dependencies=[Security(get_current_user, scopes=['users:update'])],
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserServiceDep,
):
    user = await service.update(user_id, user_data)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    return user


@router.put(
    '/{user_id}/roles',
    response_model=UserPublic,
    dependencies=[Security(get_current_user, scopes=['roles:update'])],
)
async def update_user_roles(
    user_id: int,
    roles_data: UserRolesUpdate,
    service: UserServiceDep,
):
    try:
        user = await service.update_roles(
            user_id=user_id,
            role_names=roles_data.roles,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    return user


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['users:delete'])],
)
async def delete_user(user_id: int, service: UserServiceDep):
    deleted = await service.delete(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )
