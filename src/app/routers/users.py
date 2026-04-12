from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.services import UserServiceDep
from app.schemas.user import UserCreate, UserPublic, UserUpdate
from app.schemas.user_filters import UserFilters

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserPublic])
async def get_users(
    service: UserServiceDep,
    filters: UserFilters = Depends(),
):
    return await service.get_all(
        skip=filters.skip,
        limit=filters.limit,
        email=filters.email,
        role=filters.role,
        group_id=filters.group_id,
        search=filters.search,
    )


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: int, service: UserServiceDep):
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, service: UserServiceDep):
    try:
        return await service.create(user_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put("/{user_id}", response_model=UserPublic)
async def update_user(user_id: int, user_data: UserUpdate, service: UserServiceDep):
    user = await service.update(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserServiceDep):
    deleted = await service.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )