from pydantic import BaseModel

from datetime import datetime


class CreateNewDifficultyRequest(BaseModel):
    level: int
    name: str
    created_at: datetime
    updated_at: datetime
