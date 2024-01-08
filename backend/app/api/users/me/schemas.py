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
