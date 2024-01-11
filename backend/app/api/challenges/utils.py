from fastapi import HTTPException, status

from .models import Challenge


def input_sanitizer(body, db):
    challenge_name = db.query(Challenge).filter(Challenge.title == body.title).first()
    if challenge_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Challenge title already exists"
        )
    if len(body.title) > 50:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Title too long"
        )