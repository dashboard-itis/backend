from typing import Optional

from app.schemas.base import CommonListFilters


class PrivacyPolicyFilters(CommonListFilters):
    group_id: Optional[int] = None
    rating_mode: Optional[str] = None
