
from datetime import datetime

from pydantic import BaseModel


class CreateChallengeRequest(BaseModel):
    title: str
    description: str
    value: int
    is_hidden: bool = True
    flag: str
    flag_case_sensitive: bool = False
    challenge_type: str = 'NORMAL'
    difficulty_id: str
    parent_id: str
    category_id: str
    created_at: datetime
    updated_at: datetime
