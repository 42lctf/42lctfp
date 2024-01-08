import re
import requests

from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from sqlmodel import Session
from app.db import get_session
from app.api.users.models import User
from app.api.campus.utils import get_or_create_campus
from uuid import uuid4

from app.env_utils import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()


def verify_password(plain_password, hashed_pass):
    return pwd_context.verify(plain_password, hashed_pass)


def hash_password(password):
    return pwd_context.hash(password)


def password_validation(password: str):
    if len(password) < 6:
        return "Password length must be greater than 6 characters", False
    if not any(char.isdigit() for char in password):
        return "Password must contain at least 1 digit", False
    if not any(char.isupper() for char in password):
        return "Password should contain at least 1 upper character", False
    if not any(char.islower() for char in password):
        return "Password must contain at least 1 lower character", False
    if not any((char.isprintable() and not char.isalnum()) for char in password):
        return "Password must contain at least 1 symbol", False
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
    if credentials.nickname.empty:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Nickname can't be empty"
        )
    if len(credentials.nickname) > 50:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Nickname too long"
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
    response = requests.post('https://api.intra.42.fr/oauth/token', data=data)
    auth_token = response.json()['access_token']
    return auth_token


def get_data_from_intra(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
    user_id = response.json()['id']
    email = response.json()['email']
    nickname = response.json()['login']
    try:
        selected_title = next(filter(lambda x: x['selected'], response.json()['titles_users']), None)

        if selected_title is not None:
            title = next(filter(lambda x: selected_title['id'] == x['id'], response.json()['titles']), None)

            nickname = title['name'].replace('%login', nickname)
    except:
        pass

    campus_users = response.json()['campus_users']
    campus_info = next(filter(lambda x: x['is_primary'], campus_users), None)
    campus_id = campus_info['campus_id'] if (campus_info is not None) else None

    campus = response.json()['campus']
    campus_obj = next(filter(lambda x: (campus_id is not None and x['id'] == campus_id), campus), None)

    return {'user_id': user_id, 'nickname': nickname, 'email': email, 'campus': campus_obj}


def create_user(data, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.intra_user_id == data['user_id']).first()
    campus_t = get_or_create_campus(data['campus'], db)
    if not user:
        user_name = db.query(User).filter(User.nickname == data['nickname']).first()
        if user_name:
            # TODO: create a unique name
            pass
        user = User(
            id=uuid4(),
            email=data['email'],
            nickname=data['nickname'],
            campus_id=campus_t.id,
            intra_user_id=data['user_id'],
            is_admin=False,
            is_hidden=False,
            is_verified=True,
            is_2fa_enabled=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
