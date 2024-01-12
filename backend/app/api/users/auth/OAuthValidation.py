from typing import Optional

from jose import jwt, JWTError
from fastapi import Request, HTTPException

from fastapi.security import OAuth2

from app.env_utils import *


class OAuth2PasswordBearer(OAuth2):
    async def __call__(self, request: Request):
        exception = HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
        authorization: str = request.cookies.get('access_token')

        if not authorization:
            raise exception
        try:
            payload = jwt.decode(authorization, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise exception
        return payload
