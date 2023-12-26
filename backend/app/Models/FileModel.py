from pydantic import BaseModel
from fastapi import UploadFile, File
from uuid import UUID

class File(BaseModel):
    id: UUID
    challenge_id: UUID
    file: UploadFile = File(...)