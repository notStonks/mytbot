import hashlib
import random
import string
from datetime import datetime, timedelta

from sqlalchemy import select, delete, update, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import engine

from models import User
from api.schemas import UserInDB, UserToCreate, UserBase


async def get_user_by_email(email: str):
    """ Возвращает информацию о пользователе """
    async with AsyncSession(bind=engine) as session:
        stmt = select(User.id, User.email, User.name, User.hashed_password, User.is_active).where(User.email == email)
        result = await session.execute(stmt)
        try:
            return result.all()[0]._mapping
        except:
            return None


async def create_user(user: UserToCreate):
    """Создает в запись о пользователе в БД"""
    async with AsyncSession(bind=engine) as session:
        new_user = User(email=user.email, name=user.name, hashed_password=user.password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        user_dict = dict(new_user.__dict__)
        user_dict.pop('_sa_instance_state', None)
        return user_dict
