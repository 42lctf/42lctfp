from jose import JWTError
from sqlalchemy import or_
from app.api.users.auth.utils import *


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
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def user_login_service(user_credentials, db):
    user = db.query(User).filter(
        or_(User.email == user_credentials.email_or_name, User.nickname == user_credentials.email_or_name),
        User.password != None
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )
    chk = verify_password(user_credentials.password, user.password)
    if not chk:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    access_token = create_token(data={"sub": str(user.id)}, t="access")
    refresh_token = create_token(data={"sub": str(user.id)})
    return access_token, refresh_token


def user_auth_callback_service(code, db):
    token_intra = get_token_from_intra(code)
    data = get_data_from_intra(token_intra)

    if data['campus'] is None or data['campus']['id'] != 47:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This platform is not opened for your campus YET!"
        )
    user = create_user(data, db)
    access_token = create_token(data={"sub": str(user.id)}, t="access")
    refresh_token = create_token(data={"sub": str(user.id)})
    return access_token, refresh_token


def create_refresh_token(token: str, db: Session):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        if user_id is None:
            raise http_exception
        refresh_token_exp = payload.get('exp')
        if datetime.utcnow() > datetime.fromtimestamp(refresh_token_exp):
            raise http_exception
        token = create_token(data={"sub": user_id})
        return token
    except JWTError:
        raise http_exception
