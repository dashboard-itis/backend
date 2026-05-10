from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import GroupServiceDep
from app.models.group import GroupCreate, GroupPublic, GroupUpdate
from app.schemas.base import PaginatedResponse
from app.schemas.group_filters import GroupFilters

router = APIRouter(prefix='/groups', tags=['Groups'])

GroupFiltersDep = Annotated[GroupFilters, Depends()]


@router.get(
    '/',
    response_model=PaginatedResponse[GroupPublic],
    dependencies=[Security(get_current_user, scopes=['groups:list'])],
)
async def get_groups(
    service: GroupServiceDep,
    filters: GroupFiltersDep,
):
    return await service.get_all(filters)


@router.get(
    '/{group_id}',
    response_model=GroupPublic,
    dependencies=[Security(get_current_user, scopes=['groups:read'])],
)
async def get_group(group_id: int, service: GroupServiceDep):
    group = await service.get_by_id(group_id)

    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )

    return group


@router.post(
    '/',
    response_model=GroupPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['groups:create'])],
)
async def create_group(group_data: GroupCreate, service: GroupServiceDep):
    try:
        return await service.create(group_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    '/{group_id}',
    response_model=GroupPublic,
    dependencies=[Security(get_current_user, scopes=['groups:update'])],
)
async def update_group(
    group_id: int,
    group_data: GroupUpdate,
    service: GroupServiceDep,
):
    group = await service.update(group_id, group_data)

    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )

    return group


@router.delete(
    '/{group_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['groups:delete'])],
)
async def delete_group(group_id: int, service: GroupServiceDep):
    deleted = await service.delete(group_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )
