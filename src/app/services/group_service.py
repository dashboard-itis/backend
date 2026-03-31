from app.dependencies.session import SessionDep
from app.utils.repository import Repository
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate, GroupPublic
from typing import Optional


class GroupService:
    def __init__(self, db: SessionDep):
        self.db = db
        self.repo = Repository[Group](db, Group)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        year: Optional[int] = None,
        search: Optional[str] = None
    ) -> list[GroupPublic]:

        filters = {}
        if name:
            filters["name"] = name
        if year:
            filters["year"] = year

        groups = await self.repo.get_all(
            skip=skip,
            limit=limit,
            filters=filters,
            search=search
        )

        return [GroupPublic.model_validate(g) for g in groups]

    async def get_by_id(self, group_id: int) -> Optional[GroupPublic]:
        group = await self.repo.get(group_id)
        return GroupPublic.model_validate(group) if group else None

    async def get_by_name(self, name: str) -> Optional[GroupPublic]:
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

    async def update(self, group_id: int, group_data: GroupUpdate) -> Optional[GroupPublic]:
        update_data = group_data.model_dump(exclude_unset=True)

        group = await self.repo.update(group_id, **update_data)
        return GroupPublic.model_validate(group) if group else None

    async def delete(self, group_id: int) -> bool:
        group = await self.repo.delete(group_id)
        return group is not None