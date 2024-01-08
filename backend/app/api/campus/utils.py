from app.db import get_session
from fastapi import Depends
from sqlmodel import Session
from .models import Campus
from uuid import uuid4


def get_or_create_campus(cmp, db: Session = Depends(get_session)):
    # cmp = campus
    campus = db.query(Campus).filter(Campus.intra_campus_id == cmp['id']).first()
    if not campus:
        campus = Campus(
            id=uuid4(),
            intra_campus_id=cmp['id'],
            name=cmp['name'],
            country=cmp['country']
        )
        db.add(campus)
        db.commit()
        db.refresh(campus)
    return campus
