import os

from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import get_session
from .schemas import UserRegistrationRequest, UserLoginRequest
from . import services

UserAuthRouter = APIRouter()


@UserAuthRouter.post('/register', status_code=status.HTTP_201_CREATED)
async def user_registration(user_credentials: UserRegistrationRequest, db: Session = Depends(get_session)):
    user = await services.user_registration_service(user_credentials, db)
    if user:
        return {"message": "User registration successful"}


@UserAuthRouter.post('/login', status_code=status.HTTP_200_OK)
async def user_login(user_credentials: UserLoginRequest, db: Session = Depends(get_session)):
    access_token, refresh_token = services.user_login_service(user_credentials, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@UserAuthRouter.get('/auth/authorize', response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def auth_authorize():
    uri = (f"https://api.intra.42.fr/oauth/authorize?client_id={os.getenv('AUTH_CLIENT_ID')}"
           f"&redirect_uri={os.getenv('REDIRECT_AUTH_URL')}&response_type=code")
    return uri


@UserAuthRouter.get('/auth/callback', status_code=status.HTTP_200_OK)
async def auth_callback(code: str, response: Response, db: Session = Depends(get_session)):
    access_token, refresh_token = services.user_auth_callback_service(code, db)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return {
        "token_type": "bearer"
    }


@UserAuthRouter.get('/auth/refresh_token', status_code=status.HTTP_200_OK)
async def get_refresh_token(token: str, db: Session = Depends(get_session)):
    token = services.create_refresh_token(token, db)
    return {"refresh_token": token}
