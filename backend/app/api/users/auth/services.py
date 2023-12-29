from fastapi import HTTPException, status
from ..models import User
from uuid import uuid4
from sqlalchemy import or_
from .utils import input_sanitizer, hash_password, verify_password, create_token


async def user_registration_service(credentials, db):
    input_sanitizer(credentials, db)
    hashed_pass = hash_password(credentials.password)
    new_user = User(
        id=uuid4(),
        email=credentials.email,
        password=hashed_pass,
        nickname=credentials.nickname,
        score=0,
        is_admin=False,
        is_hidden=False,
        is_verified=False,
        created_at=credentials.created_at
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def user_login_service(user_credentials, db):
    user = db.query(User).filter(
        or_(User.email == user_credentials.email_or_name, User.nickname == user_credentials.email_or_name)
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist"
        )
    chk = verify_password(user_credentials.password, user.password)
    if not chk:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    return create_token(data={"sub": str(user.id)}, t="access")
