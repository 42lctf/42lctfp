from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status, Cookie, Depends
from sqlalchemy.orm import Session

from . import services
from .schemas import UpdateUserProfileRequest
from ..general_utils import get_user_by_token

from app.db import get_session

AdminRouter = APIRouter()


@AdminRouter.patch("/admin/update_user/{user_id}", status_code=status.HTTP_200_OK)
async def set_as_admin(user_id: str, user_information: UpdateUserProfileRequest,
                       access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    print("[DEBUG] : ", access_token)
    user = get_user_by_token(access_token, db)
    if not user.is_user_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update user profile"
        )
    services.update_user_profile(user_id, user_information, db, user)
    return {"message": "User profile updated successfully"}
