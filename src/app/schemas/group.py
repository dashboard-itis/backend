from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class GroupBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=2000, le=2100)
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=2000, le=2100)
    description: Optional[str] = None

class GroupPublic(GroupBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True