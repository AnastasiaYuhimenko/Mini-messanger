from fastapi import APIRouter, Depends, status
from ..schemas.user import UserCreate, UserLogin
from ..db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.users import register, login, get_current_user
from fastapi import HTTPException
from sqlalchemy.future import select
from ..models.user import User
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bearer_scheme = HTTPBearer()


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
    await register(user=user, db=db)
    return {"message": "Пользователь создан"}


@router.post("/login/", tags=["users"], status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_session)):
    user_excist = (
        (await db.execute(select(User).where(User.phone_number == user.phone_number)))
        .scalars()
        .first()
    )
    if not user_excist:
        raise HTTPException(status_code=404, detail="Такого пользователя не существует")

    password_correct = user_excist.hashed_password

    return await login(user=user, hashed_password=password_correct)


@router.get("/authorize/", tags=["users"], status_code=status.HTTP_200_OK)
async def authorize_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_session),
):
    return await get_current_user(token=token, db=db)
