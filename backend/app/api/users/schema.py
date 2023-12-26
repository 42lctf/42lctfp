from .models import User
from uuid import UUID
from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    id: UUID
    nickname: str

    class Config:
        orm_mode = True
