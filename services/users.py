from ..models.user import User
from passlib.context import CryptContext
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from ..config import Settings
import jwt
from sqlalchemy import select
from fastapi.security import HTTPBearer

settings = Settings()


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bearer_scheme = HTTPBearer()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def register(user, db):
    new_user = User(
        username=user.username,
        phone_number=user.phone_number,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)


async def login(user, hashed_password):
    if not verify_password(
        plain_password=user.password, hashed_password=hashed_password
    ):
        raise HTTPException(status_code=400, detail="Неверный пароль")

    access_token = create_access_token(data={"sub": str(user.phone_number)})
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token, db):
    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        phone_number: str = payload.get("sub")
        if phone_number is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.phone_number == phone_number))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=400, detail="Не авторизован")
    return user
