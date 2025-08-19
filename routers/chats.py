from fastapi import APIRouter, Depends, status
from ..schemas.chats import CreateChat, Сhat
from ..models.user import User
from ..models.chats import Chat as scheme_chat
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..services.users import get_current_user
from fastapi import HTTPException
from sqlalchemy.future import select
from ..services.chats import create_chat
from sqlalchemy import or_, and_

bearer_scheme = HTTPBearer()
router = APIRouter()


@router.post("/new_chat/", tags=["chats"], status_code=200)
async def new_chat(
    chat: CreateChat,
    db: AsyncSession = Depends(get_session),
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    user = await get_current_user(db=db, token=token)
    user_id = user.id

    result = await db.execute(select(User).where(User.username == chat.user2_name))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    else:
        user2id = user.id

    chat_excist = await db.execute(
        select(scheme_chat).where(
            or_(
                and_(scheme_chat.user1_id == user_id, scheme_chat.user2_id == user2id),
                and_(scheme_chat.user1_id == user2id, scheme_chat.user2_id == user_id),
            )
        )
    )
    if chat_excist.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Этот чат уже есть!")

    return await create_chat(user2id, user1_id=user_id, db=db)
