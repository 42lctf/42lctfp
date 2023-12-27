from .models import User
from sqlalchemy.orm import Session
from app.db import get_session
from fastapi import APIRouter, status, Depends
from uuid import uuid4, UUID
# import jwt
from jose import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# We can use 'openssl rand -hex 32'
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')

ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_user(cid: str, nickname: str, campus: str, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.campus_id == cid).first()
    if not user:
        user = User(id=uuid4(), campus_id=cid, nickname=nickname, campus=campus)
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_access_token(data={"sub": user.id})
    return user
