from typing import Annotated
from pydantic import BaseModel, StringConstraints, field_validator


PhoneStr = Annotated[str, StringConstraints(pattern=r"^\+7\d{10}$")]


class UserCreate(BaseModel):
    phone_number: PhoneStr
    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Пароль должен быть не короче 8 символов")
        if not any(char.isdigit() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(char.isalpha() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну букву")
        if " " in value:
            raise ValueError("Пароль не должен содержать пробелы")
        return value


class UserRead(BaseModel):
    id: int
    username: str
    phone_number: PhoneStr
