from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, Text, Enum
import enum
from app.db import Base
from datetime import datetime

class NotificationType(enum.Enum):
    TOAST = 'TOAST'
    ALERT = 'ALERT'
    BACKGROUND = 'BACKGROUND'

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(Text(),  nullable=True)
    content = Column(Text(), nullable=True)
    type = Column(Enum(NotificationType), default=NotificationType.TOAST, nullable=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=False)

    class Config:
        orm_mode = True