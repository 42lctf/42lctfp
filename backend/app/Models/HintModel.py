from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Hint(BaseModel):
    id: UUID
    challenge_id: UUID
    description: str
    cost: Optional[int] = 0

