import uuid

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from ..models import User

from .schemas import UpdateUserProfileRequest
from . import utils
from ..auth.utils import password_validation, email_validation

def set_admin(user_id: str, db: Session):
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
    if user.is_verified is not True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not verified"
        )
    if user.is_admin is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already admin"
        )
    user.is_admin = True
    db.commit()
    db.refresh(user)

def update_user_profile(user_id: str, user_informations: UpdateUserProfileRequest, db: Session):
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
    msg, chk = utils.sanitize_user_informations(user_informations)
    if not chk:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=msg
        )
    if user_informations.email is not None:
        if not email_validation(user_informations.email):
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="Invalid email"
            )
        else:
            user.email = user_informations.email
    if user_informations.password is not None:
        msg, chk = password_validation(user_informations.password)
        if not chk:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail=msg
            )
        else:
            user.password = utils.hash_password(user_informations.password)

    for attr in dir(user_informations):
       if attr[0] != '_' and getattr(user_informations, attr) is not None:
           setattr(user, attr, getattr(user_informations, attr))
    db.commit()
    db.refresh(user)
    return user
