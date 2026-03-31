from pydantic import BaseModel, Field
from typing import Optional

class CommonListFilters(BaseModel):
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum records to return")
    search: Optional[str] = Field(default=None, description="Search term")