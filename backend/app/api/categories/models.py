from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime


class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    display_order = Column(Integer(), nullable=False)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True
