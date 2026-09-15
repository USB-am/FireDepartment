import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from pydantic import EmailStr

from core.database import TSession
from modules.users.models import User


class UserRepository:
    def __init__(self, session: TSession):
        self._session = session

    async def get_user(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = select(User).where(User.id==user_id)
        return await self._session.scalar(stmt)

    async def get_user_by_email(self, user_email: EmailStr) -> Optional[User]:
        stmt = select(User).where(User.email==user_email)
        return await self._session.scalar(stmt)
    
    async def eagerly_get_user(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.id==user_id)
            .options(joinedload(User.profile))
        )
        return await self._session.scalar(stmt)
