from typing import Optional
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, validator


class NicknameUpdateRequest(BaseModel):
    nickname: str
    updated_at: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @validator('nickname')
    def validate_nickname(cls, v):
        if not v:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="Nickname must not be empty"
            )
        if len(v) > 50:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="Nickname must not be greater than 50 characters"
            )
        return v


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SetNewPasswordRequest(BaseModel):
    new_password: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UpdateUserInformationRequest(BaseModel):
    description: Optional[str]
    website: Optional[str]
    github: Optional[str]
    linkedin: Optional[str]
    twitter: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @validator('description')
    def validate_description(cls, v):
        if v is not None and len(v) > 250:
            raise ValueError("Wrong length")
        return v

    @validator('website', 'github', 'linkedin', 'twitter')
    def validate_social_length(cls, v):
        if v is not None and len(v) > 100:
            raise ValueError("Wrong length")
        return v


class UpdateProfilePictureRequest(BaseModel):
    profile_picture: bytes

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
