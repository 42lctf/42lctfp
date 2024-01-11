from uuid import uuid4

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from ..users.general_utils import get_user_by_token
from .schemas import CreateNewDifficultyRequest
from .models import Difficulty


def crete_new_difficulty(body: CreateNewDifficultyRequest, access_token: str, db: Session):
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
