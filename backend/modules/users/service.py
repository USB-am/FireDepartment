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
                status_code=409,
                detail=f'User.email={email} is not found!'
            )

        pwd_is_correct = bcrypt.checkpw(password.encode('utf-8'), user.password_hash)
        if not pwd_is_correct:
            raise HTTPException(
                status_code=401,
                detail='Invalid password!'
            )

        return user
