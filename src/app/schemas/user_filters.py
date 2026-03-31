from typing import Optional
from pydantic import EmailStr
from app.schemas.base import CommonListFilters

class UserFilters(CommonListFilters):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    group_id: Optional[int] = None