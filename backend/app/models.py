from sqlmodel import SQLModel, Field
from typing import Optional


class Users(SQLModel):
    firstname: str
    lastname: str
    nicknames: Optional[str] = None
    email: str