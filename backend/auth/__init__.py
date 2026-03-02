import hashlib
import secrets
from enum import Enum
from typing import List
from datetime import datetime

from authx import AuthX, AuthXConfig
from annotated_types import Annotated
from fastapi import HTTPException, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.models import User, SecretKeyUser
from data_base.session import get_session


TSession = Annotated[AsyncSession, Depends(get_session)]


config = AuthXConfig(
    JWT_SECRET_KEY='my_secret_key',
    JWT_TOKEN_LOCATION=['headers']
)
auth = AuthX(config=config)


def generate_secret_key(username: str) -> str:
    'Генерация уникального секретного ключа'
    timestamp = datetime.now().isoformat()
    random_part = secrets.token_hex(16)
    data = f'{username}{timestamp}{random_part}'

    return hashlib.sha256(data.encode()).hexdigest()


async def authenticate_user(session: TSession, secret_key: str = Header(..., alias='SECRET_KEY')) -> User:
    ''' Функция для аутентификации пользователя по SECRET_KEY '''
    result = await session.scalars(select(SecretKeyUser)\
        .where(SecretKeyUser.secret_key==secret_key))
    entry = result.first()
    if not entry:
        raise HTTPException(
            status_code=401,
            detail='Invalid SECRET_KEY',
            headers={'WWW-Authenticate': 'SecretKey'}
        )
    user = await session.get(User, entry.user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail='User not found'
        )
    user.last_used = datetime.now().isoformat()
    return user


class Role(Enum):
    admin = 'admin'
    manager = 'manager'
    dispatch = 'dispatch'
    reader = 'reader'


class RoleChecker:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User=Depends(authenticate_user)):
        if Role(user.role) not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail='Insufficient permissions'
            )
