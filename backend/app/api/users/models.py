from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime


class User(Base):
    __tablename__ = "ctf_users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=True)
    intra_user_id = Column(Integer(), nullable=True)
    nickname = Column(String(50), nullable=False)
    description = Column(String(150), nullable=True)
    website = Column(String(50), nullable=True)
    is_admin = Column(Boolean(), nullable=False)
    is_hidden = Column(Boolean(), nullable=False)
    is_verified = Column(Boolean(), nullable=False)
    is_2fa_enabled = Column(Boolean(), nullable=False)
    tfa_token = Column(String(length=50), nullable=True)
    campus_id = Column(UUID(as_uuid=True), ForeignKey("campus.id"), nullable=True)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True


class ChallengeAuthors(Base):
    __tablename__ = "challenge_authors"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenge.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("ctf_users.id"), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)
