from jose import jwt
from sqlmodel import Session

from . import utils
from app.env_utils import *


def get_user_by_token(db: Session, token: str):
    payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    id_user: str = payload.get("sub")
    return utils.get_user(db, id_user)
