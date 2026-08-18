from typing import Optional

import bcrypt
from fastapi import HTTPException
from pydantic import EmailStr

from core.database import TSession
from modules.users.repository import UserRepository
from modules.users.models import User


class UserService:
    def __init__(self, session: TSession):
        self._session = session
        self.repository = UserRepository(session)

    async def check_login(self, email: EmailStr, password: str) -> Optional[User]:
        user = await self.repository.get_user_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail='Invalid email or password!'
            )

        pwd_hash = password.encode('utf-8')
        pwd_is_correct = bcrypt.checkpw(pwd_hash, user.password_hash.encode('utf-8'))
        if not pwd_is_correct:
            raise HTTPException(
                status_code=401,
                detail='Invalid email or password!'
            )

        return user
