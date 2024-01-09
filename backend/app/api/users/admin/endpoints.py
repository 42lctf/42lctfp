from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status, Cookie, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from . import services

from ..models import User
from ..me.utils import get_user_payload

from app.env_utils import *
from app.db import get_session

AdminRouter = APIRouter()

def verify_auth_admin(token: str, db: Session):
    https_res = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise https_res
    payload = get_user_payload(token)
    id_user: str = payload.get("sub")
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.is_admin is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not admin",
        )


@AdminRouter.post("/admin/{user_id}/make_admin")
async def set_as_admin(user_id: str, access_token: Annotated[Union[str, None], Cookie()] = None,
                       db: Session = Depends(get_session)):
    verify_auth_admin(access_token, db)
    services.set_admin(user_id, db)
    return {"message": "User set as admin successfully"}