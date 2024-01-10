from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, BigInteger, LargeBinary
# from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime


class User(Base):
    __tablename__ = "ctf_users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=True)
    intra_user_id = Column(BigInteger(), nullable=True)
    nickname = Column(String(50), nullable=False)
    description = Column(String(250), nullable=True)
    website = Column(String(100), nullable=True)
    github = Column(String(100), nullable=True)
    linkedin = Column(String(100), nullable=True)
    twitter = Column(String(100), nullable=True)
    is_admin = Column(Boolean(), default=False, nullable=False)
    is_hidden = Column(Boolean(), default=False, nullable=False)
    is_verified = Column(Boolean(), default=False, nullable=False)
    is_2fa_enabled = Column(Boolean(), default=False, nullable=False)
    tfa_token = Column(String(length=100), nullable=True)
    profile_picture = Column(LargeBinary(), nullable=True)
    campus_id = Column(UUID(as_uuid=True), ForeignKey("campus.id"), nullable=True)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "nickname": self.nickname,
            "description": self.description,
            "website": self.website,
            "github": self.github,
            "linkedin": self.linkedin,
            "twitter": self.twitter,
            "is_admin": self.is_admin,
            "is_hidden": self.is_hidden,
            "is_verified": self.is_verified,
            "is_2fa_enabled": self.is_2fa_enabled,
            "campus_id": self.campus_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def is_user_admin(self):
        return self.is_admin


class ChallengeAuthor(Base):
    __tablename__ = "challenge_authors"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("ctf_users.id"), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True


class UserBan(Base):
    __tablename__ = "user_bans"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("ctf_users.id"), nullable=False)
    banned_until = Column(DateTime(), nullable=True)
    reason = Column(String(250), nullable=True)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True

