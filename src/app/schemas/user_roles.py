from pydantic import BaseModel, Field


class UserRolesUpdate(BaseModel):
    roles: list[str] = Field(min_length=1)
