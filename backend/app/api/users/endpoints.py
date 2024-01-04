from fastapi import APIRouter, Depends
# TODO cleanup his mess
from . import services
from app.db import get_session
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from .auth import services
from .auth.endpoints import UserAuthRouter

load_dotenv()

UserRouter = APIRouter()

UserRouter.include_router(UserAuthRouter)

# TEST endpoint
@UserRouter.get('/me')
async def get_me(token: str, db: Session = Depends(get_session)):
    user = services.get_user_by_token(db, token)
    return user
