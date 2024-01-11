from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.orm import Session

from app.db import get_session
from .schemas import ChallengeCreationRequest
from . import services

from app.api.users.auth.endpoints import UserAuthRouter


ChallengeRouter = APIRouter()

ChallengeRouter.include_router(UserAuthRouter)

@ChallengeRouter.post('/create', status_code=status.HTTP_201_CREATED)
async def create_challenge(challenge_fields: ChallengeCreationRequest, db: Session = Depends(get_session)):
    challenge = await services.challenge_creation_service(challenge_fields, db)
    if challenge:
        return {"message": "Challenge creation successful"}