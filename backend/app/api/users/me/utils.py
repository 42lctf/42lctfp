from sqlmodel import Session
from uuid import UUID

from ..models import User


def get_user(db: Session, id_user: str):
    try:
        id_user = UUID(id_user).hex
    except ValueError:
        raise ValueError("Invalid UUID")

    user = db.query(User).filter(User.id == id_user).first()
    return user
