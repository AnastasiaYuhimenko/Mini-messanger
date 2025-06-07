from pydantic import BaseModel


class Сhat(BaseModel):
    id: int
    user1_id: int
    user2_id: int


class CreateChat(BaseModel):
    user2_name: str
