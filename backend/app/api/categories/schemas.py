from pydantic import BaseModel

from datetime import datetime

class CategoryRequest(BaseModel):
    name: str
    display_order: int

class CreateNewCategoryRequest(BaseModel):
    display_order: int
    name: str
    created_at: datetime
    updated_at: datetime
