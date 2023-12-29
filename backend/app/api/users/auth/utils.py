import os
import re

from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from ..models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


load_dotenv()

# We can use 'openssl rand -hex 32'
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')

ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_pass):
    return pwd_context.verify(plain_password, hashed_pass)


def hash_password(password):
    return pwd_context.hash(password)


def password_validation(password: str):
    sym = ['@', '#', '$', '%']

    if len(password) < 6:
        return "Password length must be greater than 6 characters", False
    if not any(char.isdigit() for char in password):
        return "Password should contain at least 1 digit", False
    if not any(char.isupper() for char in password):
        return "Password should contain at least 1 upper character", False
    if not any(char.islower() for char in password):
        return "Password should contain at least 1 lower character", False
    if not any(char in sym for char in password):
        return "Password should contain at least 1 symbol [@, #, $, %]", False
    return "", True


def email_validation(email: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def input_sanitizer(credentials, db):
    user = db.query(User).filter(credentials.email == User.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already used"
        )
    msg, chk = password_validation(credentials.password)
    if not chk:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=msg
        )
    if not email_validation(credentials.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invalid email"
        )
    nickname = db.query(User).filter(credentials.nickname == User.nickname).first()
    if nickname:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nickname already taken"
        )


def create_token(data: dict, t="refresh", expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    key = JWT_REFRESH_SECRET_KEY
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        if t == "access":
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            key = JWT_SECRET_KEY
        else:
            expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=ALGORITHM)
    return encoded_jwt