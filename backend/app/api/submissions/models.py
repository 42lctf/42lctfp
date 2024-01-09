from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db import Base
from datetime import datetime


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("ctf_users.id"), nullable=False)
    content = Column(String(100), nullable=False)
    ip = Column(String(46), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True


class Solve(Base):
    __tablename__ = "solves"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("ctf_users.id"), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True
