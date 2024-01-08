from datetime import datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError
from sqlmodel import Session

from . import utils
from .schemas import NicknameUpdateRequest, ChangePasswordRequest, SetNewPasswordRequest, UpdateUserInformationRequest
from ..models import User
from ..auth.utils import password_validation, verify_password, hash_password
from app.env_utils import *


def get_user_by_token(token: str, db: Session):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    id_user: str = payload.get("sub")
    return utils.get_user(db, id_user)


def update_user_nickname(token: str, body: NicknameUpdateRequest, db: Session):
    payload = utils.get_user_payload(token)
    id_user: str = payload.get("sub")
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    utils.sanitize_nickname(body.nickname, db)
    user.nickname = body.nickname
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)

    return user


def update_user_password(token: str, body: ChangePasswordRequest, db: Session):
    payload = utils.get_user_payload(token)
    id_user: str = payload.get("sub")
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.password is None:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="User doesn't have a password"
        )
    msg, chk = password_validation(body.new_password)
    if not chk:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=msg
        )
    chk = verify_password(body.old_password, user.password)
    if not chk:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    body.new_password = hash_password(body.new_password)
    user.password = body.new_password
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)


def set_user_password(token: str, body: SetNewPasswordRequest, db: Session):
    payload = utils.get_user_payload(token)
    id_user: str = payload.get("sub")
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.password is not None:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="User already has a password"
        )
    msg, chk = password_validation(body.new_password)
    if not chk:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=msg
        )
    body.new_password = hash_password(body.new_password)
    user.password = body.new_password
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)


def update_user_profile(token: str, body: UpdateUserInformationRequest, db: Session):
    payload = utils.get_user_payload(token)
    id_user: str = payload.get("sub")
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    msg, chk = utils.check_field_lens(body)
    if not chk:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=msg
        )
    user.description = body.description
    user.website = body.website
    user.github = body.github
    user.linkedin = body.linkedin
    user.twitter = body.twitter
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
