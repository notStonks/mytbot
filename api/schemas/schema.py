import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr, UUID4, validator


class Medicine(BaseModel):
    user_id: int
    name: str
    number_of_receptions: int = Field(default=1)
    time_of_reception: int  # время приема (в зависимости от пищи, до, во время или после нее) 0-3
    notifications: bool
    times: List[datetime.time]


class UserBase(BaseModel):
    """ Формирует тело ответа с деталями пользователя """
    id: int
    email: EmailStr
    name: str
    is_active: bool


class UserInDB(UserBase):
    """ Проверяет sign-up запрос """
    hashed_password: str


class UserToCreate(BaseModel):
    """Для создания записи в бд"""
    email: EmailStr
    name: str
    password: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
