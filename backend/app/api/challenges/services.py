
from app.api.users.auth.utils import *

from sqlalchemy.orm import Session

from uuid import uuid4
from ..users.general_utils import get_user_by_token
from .schemas import ChallengeCreationRequest
from .models import Challenge
from .utils import input_sanitizer

def create_new_challenge_request(body: ChallengeCreationRequest, access_token: str, db: Session):
    user = get_user_by_token(access_token, db)
    if not user.is_user_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create challenge"
        )
   # input_sanitizer(body, db)
    new_challenge = Challenge(
        id=uuid4(),
        title=body.title,
        description=body.description,
        value=body.value,
        is_hidden=body.is_hidden,
        difficulty_id=body.difficulty_id,
        flag=body.flag,
        flag_case_sensitive=body.flag_case_sensitive,
        parent_id=body.parent_id,
        category_id=body.category_id,
        challenge_type=body.challenge_type,
    )
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)