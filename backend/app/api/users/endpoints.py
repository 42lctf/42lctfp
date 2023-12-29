from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
# TODO cleanup his mess
from . import services
from app.db import get_session
import os
from dotenv import load_dotenv
import requests
from sqlalchemy.orm import Session
from app.api.users.auth.schemas import UserRegistrationRequest
from .auth.services import user_registration_service

load_dotenv()

UserRouter = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@UserRouter.get('/auth/callback')
async def auth_callback(code: str, db: Session = Depends(get_session)):
    data = {
        'grant_type': (None, 'authorization_code'),
        'client_id': (None, os.getenv('AUTH_CLIENT_ID')),
        'client_secret': (None, os.getenv('AUTH_CLIENT_SECRET')),
        'code': (None, code),
        'redirect_uri': (None, os.getenv('REDIRECT_AUTH_URL'))
    }
    response = requests.post('https://api.intra.42.fr/oauth/token', files=data)

    auth_token = response.json()['access_token']

    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)

    user_id = response.json()['id']
    nickname = response.json()['login']
    campus = response.json()['campus'][0]['name']
    email = response.json()['email']

    if campus != "Lausanne":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This platform is not opened for your campus YET!"
        )

    new_user = await services.create_user(user_id, nickname, campus, db)
    token = services.create_access_token(data={"sub": str(new_user.id)})
    if new_user:
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong"
        )


@UserRouter.get('/me')
async def get_me(token: str, db: Session = Depends(get_session)):
    user = services.get_user_by_token(db, token)
    return user


@UserRouter.post('/register', status_code=status.HTTP_201_CREATED)
async def user_registration(user_credentials: UserRegistrationRequest, db: Session = Depends(get_session)):
    user = await user_registration_service(user_credentials, db)
    if user:
        return {"message": "User registration successful"}

# @UserRouter.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}
