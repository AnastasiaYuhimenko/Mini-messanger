from sqlalchemy import Column, Integer, String
from db.base import Base
from datetime import datetime
from sqlalchemy import DateTime


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True)
    sender_id = Column(Integer, index=True)
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
