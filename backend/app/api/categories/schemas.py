from pydantic import BaseModel

from datetime import datetime


class CreateNewCategoryRequest(BaseModel):
    display_order: int
    name: str
    created_at: datetime
    updated_at: datetime
