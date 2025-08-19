from pydantic import BaseModel


class Message(BaseModel):
    # chat_id: int
    username: str
    text: str


class ReadMessages(BaseModel):
    user2_name: str
