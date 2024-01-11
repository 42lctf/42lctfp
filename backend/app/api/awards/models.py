from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, Text, ForeignKey, String, Integer
from app.db import Base
from datetime import datetime

class Award(Base):
    __tablename__ = "awards"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("ctf_users.id"), nullable=False)
    name = Column(String(80), nullable=True)
    reason = Column(Text(), nullable=True)
    value = Column(Integer(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True