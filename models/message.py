from sqlalchemy import Column, Integer, String, func
from db.base import Base
from sqlalchemy import DateTime


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True)
    sender_id = Column(Integer, index=True)
    text = Column(String)
    timestamp = Column(DateTime, server_default=func.now())
