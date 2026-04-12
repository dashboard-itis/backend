from typing import Optional

from app.dependencies.repositories import GroupRepositoryDep
from app.schemas.group import GroupCreate, GroupPublic, GroupUpdate


class GroupService:
    def __init__(self, repo: GroupRepositoryDep):
        self.repo = repo

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        search: Optional[str] = None,
    ) -> list[GroupPublic]:
        filters = {
            "name": name,
        }
        filters = {key: value for key, value in filters.items() if value is not None}

        groups = await self.repo.get_all(
            skip=skip,
            limit=limit,
            filters=filters,
            search=search,
        )
        return [GroupPublic.model_validate(group) for group in groups]

    async def get_by_id(self, group_id: int) -> GroupPublic | None:
        group = await self.repo.get(group_id)
        return GroupPublic.model_validate(group) if group else None

    async def get_by_name(self, name: str) -> GroupPublic | None:
        groups = await self.repo.get_all(filters={"name": name}, limit=1)
        if not groups:
            return None
        return GroupPublic.model_validate(groups[0])

    async def create(self, group_data: GroupCreate) -> GroupPublic:
        existing = await self.get_by_name(group_data.name)
        if existing:
            raise ValueError("Group name already exists")

        group = await self.repo.create(**group_data.model_dump())
        return GroupPublic.model_validate(group)

    async def update(self, group_id: int, group_data: GroupUpdate) -> GroupPublic | None:
        update_data = group_data.model_dump(exclude_unset=True)
        group = await self.repo.update(group_id, **update_data)
        return GroupPublic.model_validate(group) if group else None

    async def delete(self, group_id: int) -> bool:
        deleted = await self.repo.delete(group_id)
        return deleted is not None