from fastapi import APIRouter, Depends
from ..schemas.message import Message, ReadMessages
from ..models.chats import Chat
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..services.users import get_current_user
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import or_, and_
from ..models.message import Message as Message_bd
from ..models.user import User

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.post("/{chat_id}/messages/", tags=["chats"], status_code=200)
async def message(
    message: Message,
    db: AsyncSession = Depends(get_session),
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    user = await get_current_user(db=db, token=token)
    user_id = user.id
    user2 = await db.execute(select(User).where(User.username == message.username))
    user2 = user2.scalars().first()
    if user2 is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь, которому вы пытаетесь написать не зарегестрирован или чат не найден",
        )
    user2_id = user2.id

    chat = await db.execute(
        select(Chat).where(
            or_(
                and_(
                    Chat.user1_id == user_id,
                    Chat.user2_id == user2_id,
                ),
                and_(Chat.user1_id == user2_id, Chat.user2_id == user_id),
            )
        )
    )
    chat = chat.scalars().first()

    if chat is None:
        raise HTTPException(status_code=404, detail="Чат не найден")

    chat_id = chat.id

    message = Message_bd(
        chat_id=chat_id,
        sender_id=user_id,
        text=message.text,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)

    return {"status_code": "200 OK"}


@router.post("/{chat_id}/read_messages/", tags=["chats"], status_code=200)
async def read_messages(
    chat: ReadMessages,
    db: AsyncSession = Depends(get_session),
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    user = await get_current_user(db=db, token=token)
    user_id = user.id
    user2 = await db.execute(select(User).where(User.username == chat.user2_name))
    user2 = user2.scalars().first()
    if user2 is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь, которому вы пытаетесь написать не зарегестрирован или чат не найден",
        )
    user2_id = user2.id

    chat = await db.execute(
        select(Chat).where(
            or_(
                and_(Chat.user1_id == user_id, Chat.user2_id == user2_id),
                and_(Chat.user1_id == user2_id, Chat.user2_id == user_id),
            )
        )
    )
    chat = chat.scalars().first()

    if chat is None:
        raise HTTPException(status_code=404, detail="Чат не найден")

    chat_id = chat.id

    messages = await db.execute(select(Message_bd).where(Message_bd.chat_id == chat_id))
    messages = messages.scalars().all()
    messages_by_sender = {}

    for msg in messages:
        messages_by_sender.setdefault(msg.sender_id, []).append(msg.text)

    return messages_by_sender
