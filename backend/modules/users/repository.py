import uuid
from typing import Optional

from sqlalchemy import select
from pydantic import EmailStr

from core.database import TSession
from modules.users.models import User


class UserRepository:
    def __init__(self, session: TSession):
        self._session = session

    async def get_user(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = select(User).where(User.id==user_id)
        result = self._session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, user_email: EmailStr) -> Optional[User]:
        stmt = select(User).where(User.email==user_email)
        return await self._session.scalar(stmt)
