from ..models.chats import Chat
from sqlalchemy.future import select


async def create_chat(
    user2id,
    user1_id,
    db,
):
    new_chat = Chat(user1_id=user1_id, user2_id=user2id)
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)

    return new_chat.id
