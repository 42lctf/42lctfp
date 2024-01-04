from typing import Annotated

from fastapi import APIRouter, Depends, status, Header, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db import get_session
from app.env_utils import *
from . import services
from .schemas import NicknameUpdateRequest

MeRouter = APIRouter()


def verify_auth(token: str):
    try:
        jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@MeRouter.get('/me', status_code=status.HTTP_200_OK)
async def get_me(token: Annotated[str, Header()], db: Session = Depends(get_session)):
    verify_auth(token)
    user = services.get_user_by_token(token, db)
    return user


@MeRouter.patch('/me/change_nickname', status_code=status.HTTP_201_CREATED)
async def update_nickname(token: Annotated[str, Header()], body: NicknameUpdateRequest,
                          db: Session = Depends(get_session)):
    verify_auth(token)
    user = services.update_user_nickname(token, body, db)
    return user
