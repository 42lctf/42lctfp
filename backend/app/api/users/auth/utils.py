import os
import re
import requests

from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from sqlmodel import Session
from uuid import uuid4
from app.db import get_session
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
        return "Password must contain at least 1 digit", False
    if not any(char.isupper() for char in password):
        return "Password should contain at least 1 upper character", False
    if not any(char.islower() for char in password):
        return "Password must contain at least 1 lower character", False
    if not any(char in sym for char in password):
        return "Password must contain at least 1 symbol [@, #, $, %]", False
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
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Email already used"
        )
    msg, chk = password_validation(credentials.password)
    if not chk:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=msg
        )
    if not email_validation(credentials.email):
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Invalid email"
        )
    nickname = db.query(User).filter(credentials.nickname == User.nickname).first()
    if nickname:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
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


def get_token_from_intra(code):
    data = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv('AUTH_CLIENT_ID'),
        'client_secret': os.getenv('AUTH_CLIENT_SECRET'),
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_AUTH_URL')
    }
    response = requests.post('https://api.intra.42.fr/oauth/token', files=data)
    auth_token = response.json()['access_token']
    return auth_token


def get_data_from_intra(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
    user_id = response.json()['id']
    nickname = response.json()['login']
    campus = response.json()['campus'][0]['id']
    email = response.json()['email']

    return [user_id, nickname, campus, email]


def create_user(data, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.intra_id == data[0]).first()
    if not user:
        user_name = db.query(User).filter(User.nickname == data[1]).first()
        if user_name:
            #TODO: create a unique name
            pass
        user = User(
            id=uuid4(),
            email=data[3],
            nickname=data[1],
            campus=data[2],
            intra_id=data[0],
            score=0,
            is_admin=False,
            is_hidden=False,
            is_verified=True,
            created_at=datetime.now()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        # user = db.query(User).filter(User.intra_id == data[0]).first()
    return user
