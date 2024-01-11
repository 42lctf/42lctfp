from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime


class Difficulty(Base):
    __tablename__ = "difficulties"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    level = Column(Integer(), nullable=False)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime(), default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.utcnow(), nullable=False)

    class Config:
        orm_mode = True
