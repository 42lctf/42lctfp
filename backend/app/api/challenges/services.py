
from app.api.users.auth.utils import *
from app.api.challenges.models import Challenge

async def challenge_creation_service(challenge_fields, db):
 #   input_sanitizer(challenge_fields, db)
    new_challenge = Challenge(
        id=uuid4(),
        title=challenge_fields.title,
        description=challenge_fields.description,
        value=challenge_fields.value,
        is_hidden=challenge_fields.is_hidden,
        difficulty_id=challenge_fields.difficulty_id,
        flag=challenge_fields.flag,
        flag_case_sensitive=challenge_fields.flag_case_sensitive,
        parent_id=challenge_fields.parent_id,
        category_id=challenge_fields.category_id,
        challenge_type=challenge_fields.challenge_type,
    )
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)
    return new_challenge