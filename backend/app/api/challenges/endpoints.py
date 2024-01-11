from fastapi import APIRouter, status, Cookie, Depends
from sqlalchemy.orm import Session
from typing import Annotated, Union

from app.db import get_session
from .schemas import ChallengeCreationRequest
from .services import create_new_challenge_request


ChallengeRouter = APIRouter()


@ChallengeRouter.post('/challenges/new', status_code=status.HTTP_201_CREATED)
async def create_new_challenge(body: ChallengeCreationRequest, access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    await create_new_challenge_request(body, access_token, db)
    return {"message": "Challenge creation successful"}