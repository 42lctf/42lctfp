from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy.dialects.postgresql import UUID
from .models import ChallengeType

class ChallengeCreationRequest(BaseModel):
    title: str
    description: str
    value: int
    is_hidden: bool
    difficulty_id: str
    flag: str
    flag_case_sensitive: bool
    parent_id: str
    category_id: str
    challenge_type: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True