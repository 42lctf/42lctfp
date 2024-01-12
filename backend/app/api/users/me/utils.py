from sqlmodel import Session
from uuid import UUID
from fastapi import HTTPException, status
from ..models import User
from jose import jwt, JWTError
from app.env_utils import *
from .schemas import UpdateUserInformationRequest


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


def check_field_lens(body: UpdateUserInformationRequest):
    errors = []
    if len(body.description) > 250:
        errors.append("Description too long")
    if len(body.website) > 100:
        errors.append("Website too long")
    if len(body.github) > 100:
        errors.append("Github too long")
    if len(body.linkedin) > 100:
        errors.append("LinkedIn too long")
    if len(body.twitter) > 100:
        errors.append("Twitter too long")

    return " | ".join(errors), len(errors) == 0
