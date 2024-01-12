import uuid

from fastapi import HTTPException, status, __version__
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.env_utils import *

from .models import User

import deprecation


@deprecation.deprecated(deprecated_in="1.0", removed_in="2.0",
                        current_version=__version__,
                        details="Use the bar function instead")
def get_user_payload(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Couldn't validate credentials"
        )
    return payload


@deprecation.deprecated(deprecated_in="1.0", removed_in="2.0",
                        current_version=__version__,
                        details="Use the bar function instead")
def get_user_by_token(token: str, db: Session) -> User:
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = get_user_payload(token)
    id_user: str = payload.get("sub")
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_user_by_payload(payload, db):
    id_user: str = payload.get("sub")
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_user_by_id(user_id: str, db: Session) -> User:
    try:
        user_id = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user id"
        )
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
