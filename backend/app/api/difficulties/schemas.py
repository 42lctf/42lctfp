from pydantic import BaseModel

from datetime import datetime

class DifficultyRequest(BaseModel):
    level: int
    name: str

class CreateNewDifficultyRequest(BaseModel):
    level: int
    name: str
    created_at: datetime
    updated_at: datetime

class PatchDifficultyRequest(BaseModel):
    level: int
    name: str
    updated_at: datetime = datetime.utcnow()