from .schemas import UpdateUserProfileRequest


def sanitize_user_information(user_information: UpdateUserProfileRequest):
    errors = []

    if user_information.nickname is not None:
        if len(user_information.nickname) > 50:
            errors.append("Nickname too long")
    if user_information.description is not None:
        if len(user_information.description) > 250:
            errors.append("Description too long")
    if user_information.website is not None:
        if len(user_information.website) > 100:
            errors.append("Website too long")
    if user_information.github is not None:
        if len(user_information.github) > 100:
            errors.append("Github too long")
    if user_information.linkedin is not None:
        if len(user_information.linkedin) > 100:
            errors.append("Linkedin too long")
    if user_information.twitter is not None:
        if len(user_information.twitter) > 100:
            errors.append("Twitter too long")

    return " | ".join(errors), len(errors) == 0
