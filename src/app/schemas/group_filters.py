from typing import Optional
from app.schemas.base import CommonListFilters

class GroupFilters(CommonListFilters):
    name: Optional[str] = None
    year: Optional[int] = None