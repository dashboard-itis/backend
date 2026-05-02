from typing import Optional

from app.schemas.base import CommonListFilters


class ImportSourceFilters(CommonListFilters):
    stream_id: Optional[int] = None
    course_id: Optional[int] = None
    status: Optional[str] = None
