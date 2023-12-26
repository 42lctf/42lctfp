from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class SolutionFlag(BaseModel):
   id: UUID
   challenge_id: UUID
   flag: str
