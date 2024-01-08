from sqlmodel import Session
from uuid import UUID
from fastapi import HTTPException, status
from ..models import User


def get_user(db: Session, id_user: str):
    try:
        id_user = UUID(id_user).hex
    except ValueError:
        raise ValueError("Invalid UUID")

    user = db.query(User).filter(User.id == id_user).first()
    return user


def sanitize_nickname(nickname: str, db: Session):
    if not nickname:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Nickname must not be empty"
        )
    if len(nickname) > 50:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Nickname must not be greater than 50 characters"
        )
    nickname = db.query(User).filter(User.nickname == nickname).first()
    if nickname:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Nickname already chosen"
        )
