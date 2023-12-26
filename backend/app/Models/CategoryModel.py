from pydantic import BaseModel
from typing import LiteralString
from uuid import UUID

class Categories(BaseModel):
    id: UUID
    name: str