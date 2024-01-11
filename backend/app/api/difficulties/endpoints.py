from typing import Annotated, Union

from fastapi import APIRouter, status, Cookie, Depends
from sqlalchemy.orm import Session

from .schemas import CreateNewDifficultyRequest
from .services import crete_new_difficulty
from app.db import get_session

DifficultyRouter = APIRouter()


@DifficultyRouter.post('/difficulties/new', status_code=status.HTTP_201_CREATED)
async def create_difficulty(body: CreateNewDifficultyRequest, access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    crete_new_difficulty(body, access_token, db)
    return {"message": "New difficulty created successfully"}