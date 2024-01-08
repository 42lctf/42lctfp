from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base
from datetime import datetime


class Campus(Base):
    __tablename__ = "campus"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    intra_campus_id = Column(Integer, nullable=False)
    name = Column('name', String(50), nullable=True)
    country = Column('country', String(50), nullable=True)
    created_at = Column('created_at', DateTime, default=datetime.now(), nullable=False)
    updated_at = Column('updated_at', DateTime, default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True
