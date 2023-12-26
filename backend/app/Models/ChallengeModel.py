from pydantic import BaseModel, Field
from typing import List
from uuid import UUID

class Challenges(BaseModel):
    id: UUID
    title: str
    description: str
    difficulty: int
    flag: str
    hints: List[UUID] = []
    files: List[UUID] = []
    category_id: UUID