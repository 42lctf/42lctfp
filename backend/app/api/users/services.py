from .models import User
from sqlalchemy.orm import Session
from app.db import get_session
from fastapi import Depends, HTTPException, status
from uuid import uuid4, UUID
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
# import jwt
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

# We can use 'openssl rand -hex 32'
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')

ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


async def create_user(cid: str, nickname: str, campus: str, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.campus_id == cid).first()
    if not user:
        user = User(id=uuid4(), campus_id=cid, nickname=nickname, campus=campus, score=0, created_at=datetime.now())
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_user(db: Session, id_user: str):
    try:
        id_user = UUID(id_user).hex
    except ValueError:
        raise ValueError("Invalid UUID")

    user = db.query(User).filter(User.id == id_user).first()
    return user


def get_user_by_token(db: Session, token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    id_user: str = payload.get("sub")
    return get_user(db, id_user)





# async def email_login_service(email: str, password: str, db: Session = Depends(get_session)):
#     user = db.query(User).filter(User.email == email)
#     if not verify_password(password, user.password):
#         return None
#     return user



