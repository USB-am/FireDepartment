import hashlib
import secrets
from datetime import datetime

from annotated_types import Annotated
from fastapi import HTTPException, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.model import User, SecretKeyUser
from data_base.session import get_session


TSession = Annotated[AsyncSession, Depends(get_session)]


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
