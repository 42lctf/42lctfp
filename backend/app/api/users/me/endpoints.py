from typing import Annotated, Union

from fastapi import APIRouter, Depends, status, HTTPException, Cookie
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db import get_session
from app.env_utils import *
from . import services
from .schemas import NicknameUpdateRequest, ChangePasswordRequest, SetNewPasswordRequest, UpdateUserInformationRequest
from ..general_utils import get_user_by_payload
from ..auth.OAuthValidation import OAuth2PasswordBearer
from ..models import User

MeRouter = APIRouter()


def verify_auth(token: str):
    https_res = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise https_res
    try:
        jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise https_res


oauth2_scheme = OAuth2PasswordBearer()


@MeRouter.get('/me', status_code=status.HTTP_200_OK)
async def get_me(payload: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    user = get_user_by_payload(payload, db)
    user_dict = user.to_dict()
    del user_dict['password']
    return user_dict


@MeRouter.patch('/me/nickname', status_code=status.HTTP_201_CREATED)
async def update_nickname(body: NicknameUpdateRequest, payload: str = Depends(oauth2_scheme),
                          db: Session = Depends(get_session)):
    user = get_user_by_payload(payload, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    nickname = db.query(User).filter(User.nickname == body.nickname).first()
    if nickname:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Nickname already chosen"
        )
    user.nickname = body.nickname
    user.updated_at = body.updated_at
    db.commit()
    db.refresh(user)

    return user.nickname


@MeRouter.patch('/me/password', status_code=status.HTTP_201_CREATED)
async def update_password(body: ChangePasswordRequest, access_token: Annotated[Union[str, None], Cookie()] = None,
                          db: Session = Depends(get_session)):
    verify_auth(access_token)
    services.update_user_password(access_token, body, db)
    return {"message": "Password updated successfully"}


@MeRouter.post('/me/password', status_code=status.HTTP_201_CREATED)
async def set_password(body: SetNewPasswordRequest, access_token: Annotated[Union[str, None], Cookie()] = None,
                       db: Session = Depends(get_session)):
    verify_auth(access_token)
    services.set_user_password(access_token, body, db)
    return {"message": "Password set successfully"}


@MeRouter.patch('/me/profile', status_code=status.HTTP_201_CREATED)
async def update_profile(body: UpdateUserInformationRequest, access_token: Annotated[Union[str, None], Cookie()] = None,
                         db: Session = Depends(get_session)):
    verify_auth(access_token)
    services.update_user_profile(access_token, body, db)
    return {"message": "Profile updated successfully"}
