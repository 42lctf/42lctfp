from pydantic import BaseModel


class NicknameUpdateRequest(BaseModel):
    nickname: str

