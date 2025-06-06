from datetime import datetime  # ??
from pydantic import BaseModel


class Message(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    text: str
    timestamp: datetime
