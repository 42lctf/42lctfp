from uuid import uuid4
from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy import asc

from ..users.general_utils import get_user_by_token
from .schemas import CreateNewDifficultyRequest, PatchDifficultyRequest, DifficultyRequest
from .models import Difficulty
from app.api.challenges.models import Challenge

def get_difficulties(access_token: str, db: Session) -> List[Difficulty]:
    user = get_user_by_token(access_token, db)
    if not user.is_user_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can retrieve difficulties"
        )
    difficulties = db.query(Difficulty).order_by(asc(Difficulty.level)).all()
    if not difficulties:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No difficulties created for now"
        )
    filtered_difficulties = [
        DifficultyRequest(level=difficulty.level, name=difficulty.name)
        for difficulty in difficulties
    ]
    return filtered_difficulties

def create_new_difficulty(body: CreateNewDifficultyRequest, access_token: str, db: Session):
    user = get_user_by_token(access_token, db)
    if not user.is_user_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create new difficulty"
        )
    difficulty_name = db.query(Difficulty).filter(Difficulty.name == body.name).first()
    if difficulty_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Difficulty already exists"
        )
    if len(body.name) > 50:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Difficulty name too long"
        )
    difficulty = Difficulty(
        id=uuid4(),
        level=body.level,
        name=body.name,
        created_at=body.created_at,
        updated_at=body.updated_at
    )
    db.add(difficulty)
    db.commit()
    db.refresh(difficulty)


def update_difficulty(difficulty_id: str, body: PatchDifficultyRequest, access_token: str, db: Session):
    user = get_user_by_token(access_token, db)
    if not user.is_user_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update difficulty"
        )
    difficulty = db.query(Difficulty).filter(Difficulty.id == difficulty_id).first()
    if difficulty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Difficulty not found"
        )
    difficulty_name = db.query(Difficulty).filter(Difficulty.name == body.name, Difficulty.id != difficulty_id).first()
    if difficulty_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Difficulty name already exists"
        )
    if len(body.name) > 50:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Difficulty name too long"
        )

    difficulty.level = body.level
    difficulty.name = body.name
    difficulty.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(difficulty)


def delete_difficulty(difficulty_id: str, access_token: str, db: Session):
    user = get_user_by_token(access_token, db)
    if not user.is_user_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete difficulty"
        )
    difficulty = db.query(Difficulty).filter(Difficulty.id == difficulty_id).first()
    if difficulty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Difficulty not found"
        )
    challenges_using_difficulty = db.query(Challenge).filter(Challenge.difficulty_id == difficulty_id).all()
    if challenges_using_difficulty:
        challenge_names = [challenge.title for challenge in challenges_using_difficulty]
        challenges_str = ', '.join(challenge_names)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Difficulty is used by challenges: {challenges_str}. Cannot delete."
        )

    db.delete(difficulty)
    db.commit()
    