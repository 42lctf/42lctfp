# from sqlmodel import Field
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from app.db import Base



class User(Base):
    __tablename__ = "ctf_user"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=True)
    intra_id = Column(Integer, nullable=True)
    campus = Column(String, nullable=True)
    nickname = Column(String, nullable=False)
    description = Column(String, nullable=True)
    score = Column(Integer, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    is_hidden = Column(Boolean, nullable=False)
    is_verified = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)

    class Config:
        orm_mode = True





# class UserRegistrationResponse(Base):
#     message: String
    # data: UserResponse



