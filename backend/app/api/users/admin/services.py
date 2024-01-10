import uuid

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from ..models import User

from .schemas import UpdateUserProfileRequest
from . import utils
from ..auth.utils import password_validation, email_validation, hash_password

from ..general_utils import get_user_by_id


def set_admin(user_id: str, db: Session):
    user = get_user_by_id(user_id, db)
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


def update_user_profile(user_id: str, user_information: UpdateUserProfileRequest, db: Session, admin: User):
    user = get_user_by_id(user_id, db)
    msg, chk = utils.sanitize_user_information(user_information)
    if not chk:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=msg
        )
    if user_information.email is not None:
        if not email_validation(user_information.email):
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="Invalid email"
            )
        else:
            user.email = user_information.email
    if user_information.password is not None:
        msg, chk = password_validation(user_information.password)
        if not chk:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail=msg
            )
        else:
            user.password = hash_password(user_information.password)

    for attr in dir(user_information):
        if attr[0] != '_' and getattr(user_information, attr) is not None:
            setattr(user, attr, getattr(user_information, attr))
    db.commit()
    db.refresh(user)
    return user
