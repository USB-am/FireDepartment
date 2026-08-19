from typing import Optional

import bcrypt
from fastapi import HTTPException
from pydantic import EmailStr

from core.database import TSession
from core.security import Role
from modules.users.repository import UserRepository
from modules.users.models import User, UserProfile


class UserService:
    def __init__(self, session: TSession):
        self._session = session
        self.repository = UserRepository(session)

    async def user_is_exists(self, email: EmailStr) -> bool:
        user = await self.repository.get_user_by_email(email)
        return user is not None

    async def check_login(self, email: EmailStr, password: str) -> User:
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

    async def create_user(self, email: EmailStr, username: str, password: str) -> User:
        pwd_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(
            email=email,
            username=username,
            password_hash=pwd_hash.decode('utf-8'),
            role=Role.dispatch.value
        )
        self._session.add(user)

        return user

    async def create_user_profile(self, user: User) -> UserProfile:
        return UserProfile(
            user_id=user.id,
            user=user
        )
