from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer
from app.db import Base


class Campus(Base):
    __tablename__ = "campus"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    campus_id = Column(Integer, nullable=False)
    # name = Column('name', String(50), nullable=False)

    class Config:
        orm_mode = True
