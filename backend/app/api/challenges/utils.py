


def input_sanitizer(challenge_fields, db):
    user = db.query(User).filter(credentials.email == User.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Email already used"
        )
    msg, chk = password_validation(credentials.password)
    if not chk:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=msg
        )
    if not email_validation(credentials.email):
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Invalid email"
        )
    nickname = db.query(User).filter(credentials.nickname == User.nickname).first()
    if nickname:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Nickname already taken"
        )
    if credentials.nickname.empty:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Nickname can't be empty"
        )
    if len(credentials.nickname) > 50:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Nickname too long"
        )