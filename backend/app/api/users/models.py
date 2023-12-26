from sqlmodel import Field
# from typing import Optional
# from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean

from app.db import Base

class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    nickname = Column(String, nullable=False)
    description = Column(String, nullable=True)
    score = Column(Integer, nullable=True)
    is_admin = Column(Boolean, nullable=True)

    class Config:
        orm_mode = True
