from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# TODO cleanup his mess
from . import services
from app.db import get_session
import os
from dotenv import load_dotenv
import requests
from sqlalchemy.orm import Session
from .auth.schemas import UserRegistrationRequest, UserLoginRequest
from .auth.services import user_registration_service, user_login_service, user_auth_callback_service

load_dotenv()

UserRouter = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@UserRouter.get('/me')
async def get_me(token: str, db: Session = Depends(get_session)):
    user = services.get_user_by_token(db, token)
    return user


@UserRouter.post('/register', status_code=status.HTTP_201_CREATED)
async def user_registration(user_credentials: UserRegistrationRequest, db: Session = Depends(get_session)):
    user = await user_registration_service(user_credentials, db)
    if user:
        return {"message": "User registration successful"}


@UserRouter.post('/login', status_code=status.HTTP_200_OK)
async def user_login(user_credentials: UserLoginRequest, db: Session = Depends(get_session)):
    token = await user_login_service(user_credentials, db)
    return {"access_token": token, "token_type": "bearer"}


@UserRouter.get('/auth/callback', status_code=status.HTTP_200_OK)
async def auth_callback(code: str, db: Session = Depends(get_session)):
    token = await user_auth_callback_service(code, db)
    return {"access_token": token, "token_type": "bearer"}

# @UserRouter.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}
