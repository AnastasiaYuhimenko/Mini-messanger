from pydantic import BaseModel, ConstrainedStr


class PhoneStr(ConstrainedStr):
    regex = r"^\+7\d{10}$"


class UserCreate(BaseModel):
    phone_number: PhoneStr
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    phone_number: PhoneStr
