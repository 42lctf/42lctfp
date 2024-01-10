from .schemas import UpdateUserProfileRequest

from ..auth.utils import password_validation

def sanitize_user_informations(user_informations: UpdateUserProfileRequest):
    errors = []
    
    if user_informations.nickname is not None:
        if len(user_informations.nickname) > 50:
            errors.append("Nickname too long")
    if user_informations.description is not None:
        if len(user_informations.description) > 250:
            errors.append("Description too long")
    if user_informations.website is not None:
        if len(user_informations.website) > 100:
            errors.append("Website too long")
    if user_informations.github is not None:
        if len(user_informations.github) > 100:
            errors.append("Github too long")
    if user_informations.linkedin is not None:
        if len(user_informations.linkedin) > 100:
            errors.append("Linkedin too long")
    if user_informations.twitter is not None:
        if len(user_informations.twitter) > 100:
            errors.append("Twitter too long")
    
    return " | ".join(errors), len(errors) == 0