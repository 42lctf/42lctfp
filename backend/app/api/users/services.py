from .models import User
from .schema import UserRequest
from sqlalchemy.orm import Session
from app.db import get_session

async def create_user(db: Session, user: UserRequest):
    session = next(get_session())
    session.add(user)
    await session.commit()
    return user

# async def get_users():
#     session = next(get_session())
    # return session.exec(select(User)).all()