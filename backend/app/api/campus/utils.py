from app.db import get_session
from fastapi import Depends
from sqlmodel import Session
from .models import Campus
from uuid import uuid4


def get_or_create_campus(cid, db: Session = Depends(get_session)):
    campus = db.query(Campus).filter(Campus.campus_id == cid).first()
    if not campus:
        campus = Campus(
            id=uuid4(),
            campus_id=cid,
        )
        db.add(campus)
        db.commit()
        db.refresh(campus)
    return campus
