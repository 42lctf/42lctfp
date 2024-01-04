from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_session
from . import services

MeRouter = APIRouter()


@MeRouter.get('/me', status_code=status.HTTP_200_OK)
async def get_me(token: str, db: Session = Depends(get_session)):
    user = services.get_user_by_token(db, token)
    return user
