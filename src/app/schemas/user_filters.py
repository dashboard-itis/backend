from pydantic import EmailStr

from app.schemas.base import CommonListFilters


class UserFilters(CommonListFilters):
    email: EmailStr | None = None
    role: str | None = None
    group_id: int | None = None
