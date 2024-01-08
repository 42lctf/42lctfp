import enum

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum
from app.db import Base
from datetime import datetime


class ChallengeType(enum.Enum):
    normal = 'normal'
    docker = 'docker'


class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    value = Column(Integer(), nullable=False)
    is_hidden = Column(Boolean(), default=True, nullable=False)
    difficulty_id = Column(UUID(as_uuid=True), ForeignKey("difficulties.id"), nullable=False)
    flag = Column(String(100), nullable=False)
    flag_case_sensitive = Column(Boolean(), default=False, nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True


class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    display_order = Column(Integer(), nullable=False)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True


class Difficulty(Base):
    __tablename__ = "difficulties"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    level = Column(Integer(), nullable=False)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True
