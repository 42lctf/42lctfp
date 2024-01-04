from jose import jwt, JWTError
from fastapi import HTTPException, status
from sqlmodel import Session

from . import utils
from ..env_utils import *


def get_user_by_token(db: Session, token: str):
    try:
        payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    id_user: str = payload.get("sub")
    return utils.get_user(db, id_user)
