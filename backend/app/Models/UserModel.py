from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID

class User(SQLModel):
    id: UUID
    nickname: str
    description: Optional[str] = None
    score: int = 0
    is_admin: bool = False
    solved_challenges: list[UUID] = []
    social_medias: list[str] = []
    personal_website: Optional[str] = None