from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.future import select
from ..schemas.user import UserCreate
from ..db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from ..models.user import User

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/register/", tags=["users"], status_code=status.HTTP_201_CREATED)
async def register_new_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    registered_user = await db.execute(
        select(User).where(User.phone_number == user.phone_number)
    )
    if registered_user.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким номером телефона уже зарегестрирован",
        )
    username_excist = await db.execute(
        select(User).where(User.username == user.username)
    )

    if username_excist.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким именем уже существует, придумайте другое имя",
        )
    new_user = User(
        username=user.username,
        phone_number=user.phone_number,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "Пользователь создан"}
