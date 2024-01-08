from pydantic import BaseModel


class NicknameUpdateRequest(BaseModel):
    nickname: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


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
    description: str
    website: str
    github: str
    linkedin: str
    twitter: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UpdateProfilePictureRequest(BaseModel):
    profile_picture: bytes

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
