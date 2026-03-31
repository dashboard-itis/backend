from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.session import SessionDep
from app.services.group_service import GroupService
from app.schemas.group import GroupCreate, GroupUpdate, GroupPublic
from app.schemas.group_filters import GroupFilters

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.get("/", response_model=list[GroupPublic])
async def get_groups(
    db: SessionDep,
    filters: GroupFilters = Depends()
):
    service = GroupService(db)
    return await service.get_all(
        skip=filters.skip,
        limit=filters.limit,
        name=filters.name,
        year=filters.year,
        search=filters.search
    )

@router.get("/{group_id}", response_model=GroupPublic)
async def get_group(group_id: int, db: SessionDep):
    service = GroupService(db)
    group = await service.get_by_id(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group

@router.post("/", response_model=GroupPublic, status_code=status.HTTP_201_CREATED)
async def create_group(group_data: GroupCreate, db: SessionDep):
    service = GroupService(db)
    try:
        return await service.create(group_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{group_id}", response_model=GroupPublic)
async def update_group(group_id: int, group_data: GroupUpdate, db: SessionDep):
    service = GroupService(db)
    group = await service.update(group_id, group_data)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group

@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: int, db: SessionDep):
    service = GroupService(db)
    deleted = await service.delete(group_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")