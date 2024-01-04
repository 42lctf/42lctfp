from typing import Annotated

from fastapi import APIRouter, Depends, status, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db import get_session
from . import services
from app.env_utils import *

MeRouter = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
    user = services.get_user_by_token(db, token)
    return user
