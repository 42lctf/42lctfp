from sqlmodel import Field
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean

from app.db import Base

class User(Base):
    __tablename__ = "ctf_user"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    campus_id = Column(Integer, nullable=False)
    campus = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    description = Column(String, nullable=True)
    score = Column(Integer, nullable=False)
    is_admin = Column(Boolean, nullable=True)
    created_at = Column(String)

    class Config:
        orm_mode = True
