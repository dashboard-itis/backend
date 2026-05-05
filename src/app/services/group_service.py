from app.dependencies.repositories import GroupRepositoryDep
from app.models.group import GroupCreate, GroupPublic, GroupUpdate
from app.schemas.group_filters import GroupFilters


class GroupService:
    def __init__(self, group_repo: GroupRepositoryDep):
        self.group_repo = group_repo

    async def get_all(self, filters: GroupFilters) -> list[GroupPublic]:
        db_filters = filters.model_dump(
            exclude={'skip', 'limit', 'search'},
            exclude_none=True,
        )

        groups = await self.group_repo.fetch(
            skip=filters.skip,
            limit=filters.limit,
            filters=db_filters,
            search=filters.search,
        )
        return [GroupPublic.model_validate(group) for group in groups]

    async def get_by_id(self, group_id: int) -> GroupPublic | None:
        group = await self.group_repo.get(group_id)
        return GroupPublic.model_validate(group) if group else None

    async def get_by_name(self, name: str) -> GroupPublic | None:
        groups = await self.group_repo.fetch(filters={'name': name}, limit=1)

        if not groups:
            return None

        return GroupPublic.model_validate(groups[0])

    async def create(self, group_data: GroupCreate) -> GroupPublic:
        existing = await self.get_by_name(group_data.name)

        if existing:
            raise ValueError('Group name already exists')

        group = await self.group_repo.create(**group_data.model_dump())
        return GroupPublic.model_validate(group)

    async def update(
        self,
        group_id: int,
        group_data: GroupUpdate,
    ) -> GroupPublic | None:
        update_data = group_data.model_dump(exclude_unset=True)
        group = await self.group_repo.update(group_id, **update_data)
        return GroupPublic.model_validate(group) if group else None

    async def delete(self, group_id: int) -> bool:
        group = await self.group_repo.delete(group_id)
        return group is not None
