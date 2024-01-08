from typing import Annotated, Union

from fastapi import APIRouter, Depends, status, HTTPException, Cookie
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db import get_session
from app.env_utils import *
from . import services
from .schemas import NicknameUpdateRequest, ChangePasswordRequest, SetNewPasswordRequest

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


@MeRouter.get('/me', status_code=status.HTTP_200_OK)
async def get_me(access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    verify_auth(access_token)
    user = services.get_user_by_token(access_token, db)
    user_dict = user.to_dict()
    del user_dict['password']
    return user_dict


@MeRouter.patch('/me/change_nickname', status_code=status.HTTP_201_CREATED)
async def update_nickname(body: NicknameUpdateRequest, access_token: Annotated[Union[str, None], Cookie()] = None,
                          db: Session = Depends(get_session)):
    verify_auth(access_token)
    user = services.update_user_nickname(access_token, body, db)
    return user


@MeRouter.patch('/me/change_password', status_code=status.HTTP_201_CREATED)
async def update_password(body: ChangePasswordRequest, access_token: Annotated[Union[str, None], Cookie()] = None,
                          db: Session = Depends(get_session)):
    verify_auth(access_token)
    services.update_user_password(access_token, body, db)
    return {"message": "Password updated successfully"}


@MeRouter.patch('/me/set_password', status_code=status.HTTP_201_CREATED)
async def set_password(body: SetNewPasswordRequest, access_token: Annotated[Union[str, None], Cookie()] = None,
                       db: Session = Depends(get_session)):
    verify_auth(access_token)
    services.set_user_password(access_token, body, db)
    return {"message": "Password set successfully"}
