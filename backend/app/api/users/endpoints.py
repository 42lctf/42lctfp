from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
# TODO cleanup his mess
from . import services
from app.db import get_session
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from .auth.schemas import UserRegistrationRequest, UserLoginRequest
from .auth.services import user_registration_service, user_login_service, user_auth_callback_service, get_user_by_token

load_dotenv()

UserRouter = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@UserRouter.get('/me')
async def get_me(token: str, db: Session = Depends(get_session)):
    user = get_user_by_token(db, token)
    return user


@UserRouter.post('/register', status_code=status.HTTP_201_CREATED)
async def user_registration(user_credentials: UserRegistrationRequest, db: Session = Depends(get_session)):
    user = await user_registration_service(user_credentials, db)
    if user:
        return {"message": "User registration successful"}


@UserRouter.post('/login', status_code=status.HTTP_200_OK)
async def user_login(user_credentials: UserLoginRequest, db: Session = Depends(get_session)):
    access_token, refresh_token = await user_login_service(user_credentials, db)
    print(refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@UserRouter.get('/auth/authorize', response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def auth_authorize():
    uri = (f"https://api.intra.42.fr/oauth/authorize?client_id={os.getenv('AUTH_CLIENT_ID')}"
           f"&redirect_uri={os.getenv('REDIRECT_AUTH_URL')}&response_type=code")
    return uri


@UserRouter.get('/auth/callback', status_code=status.HTTP_200_OK)
async def auth_callback(code: str, db: Session = Depends(get_session)):
    access_token, refresh_token = await user_auth_callback_service(code, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
