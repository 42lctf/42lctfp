from pydantic import BaseModel


class NicknameUpdateRequest(BaseModel):
    nickname: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
