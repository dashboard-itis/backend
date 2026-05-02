from app.schemas.base import CommonListFilters


class GroupFilters(CommonListFilters):
    name: str | None = None
