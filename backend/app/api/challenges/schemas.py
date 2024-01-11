from datetime import datetime
from pydantic import BaseModel

class ChallengeCreationRequest(BaseModel):
    title: str
    description: str
    value: int
    is_hidden: bool = True
    difficulty_id: str
    flag: str
    flag_case_sensitive: bool = False
    parent_id: str = None
    category_id: str
    challenge_type: str = 'NORMAL'
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()