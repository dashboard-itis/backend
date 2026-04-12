from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.services import GroupServiceDep
from app.schemas.group import GroupCreate, GroupPublic, GroupUpdate
from app.schemas.group_filters import GroupFilters

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/", response_model=list[GroupPublic])
async def get_groups(
    service: GroupServiceDep,
    filters: GroupFilters = Depends(),
):
    return await service.get_all(
        skip=filters.skip,
        limit=filters.limit,
        name=filters.name,
        search=filters.search,
    )


@router.get("/{group_id}", response_model=GroupPublic)
async def get_group(group_id: int, service: GroupServiceDep):
    group = await service.get_by_id(group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )
    return group


@router.post("/", response_model=GroupPublic, status_code=status.HTTP_201_CREATED)
async def create_group(group_data: GroupCreate, service: GroupServiceDep):
    try:
        return await service.create(group_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put("/{group_id}", response_model=GroupPublic)
async def update_group(group_id: int, group_data: GroupUpdate, service: GroupServiceDep):
    group = await service.update(group_id, group_data)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )
    return group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: int, service: GroupServiceDep):
    deleted = await service.delete(group_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )