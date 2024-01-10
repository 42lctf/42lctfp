from pydantic import BaseModel

from datetime import datetime

class UpdateUserProfileRequest(BaseModel):
    email: str = None
    password: str = None
    nickname: str = None
    description: str = None
    website: str = None
    github: str = None
    linkedin: str = None
    twitter: str = None
    is_admin: bool = None
    is_hidden: bool = None
    is_verified: bool = None
    profile_picture: bytes = None
    campus_id: str = None
    updated_at: datetime