from datetime import datetime

from jose import jwt
from sqlmodel import Session

from . import utils
from .schemas import NicknameUpdateRequest
from ..models import User
from app.env_utils import *


def get_user_by_token(token: str, db: Session):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    id_user: str = payload.get("sub")
    return utils.get_user(db, id_user)


def update_user_nickname(token: str, body: NicknameUpdateRequest, db: Session):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    id_user: str = payload.get("sub")
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        pass
        # TODO : raise an exception
    user.nickname = body.nickname
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)

    return user
