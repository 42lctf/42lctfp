from typing import Annotated, Union

from fastapi import APIRouter, status, Cookie, Depends
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID

from .schemas import CreateNewDifficultyRequest
from .services import create_new_difficulty, update_difficulty, delete_difficulty
from app.db import get_session

DifficultyRouter = APIRouter()


@DifficultyRouter.post('/difficulties', status_code=status.HTTP_201_CREATED)
async def create_difficulty(body: CreateNewDifficultyRequest, access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    create_new_difficulty(body, access_token, db)
    return {"message": "New difficulty created successfully"}

@DifficultyRouter.patch('/difficulties/{difficulty_id}', status_code=status.HTTP_200_OK)
async def update_difficulty_request(difficulty_id: str, body: CreateNewDifficultyRequest, access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    update_difficulty(difficulty_id, body, access_token, db)
    return {"message": "Difficulty successfully modified"}

@DifficultyRouter.delete('/difficulties/{difficulty_id}', status_code=204)
async def delete_difficulty_request(difficulty_id: str, access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    delete_difficulty(difficulty_id, access_token, db)
    return {"message": "Difficulty successfully modified"}