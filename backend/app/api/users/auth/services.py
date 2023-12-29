import re
import os
from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from ..models import User
from uuid import uuid4, UUID

load_dotenv()

# We can use 'openssl rand -hex 32'
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')

ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(user_pass, hashed_pass):
    return pwd_context.verify(user_pass, hashed_pass)


def hash_password(password):
    return pwd_context.hash(password);


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


async def user_registration_service(credentials, db):
    input_sanitizer(credentials, db)
    hashed_pass = hash_password(credentials.password)
    new_user = User(
        id=uuid4(),
        email=credentials.email,
        password=hashed_pass,
        nickname=credentials.nickname,
        score=0,
        is_admin=False,
        is_hidden=False,
        is_verified=False,
        created_at=credentials.created_at
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
