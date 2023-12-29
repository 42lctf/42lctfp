from datetime import datetime
from pydantic import BaseModel


class UserRegistrationRequest(BaseModel):
    email: str
    password: str
    nickname: str
    created_at: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserLoginRequest(BaseModel):
    email_or_name: str
    password: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
