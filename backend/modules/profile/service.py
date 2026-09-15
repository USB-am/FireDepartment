import uuid

from fastapi import HTTPException

from core.database import TSession
from modules.users.models import UserProfile
from modules.users.repository import UserRepository
from modules.profile.repository import UserProfileRepository


class UserProfileSerice:
    def __init__(self, session: TSession):
        self._session = session
        self.repository = UserProfileRepository(session)

    async def get_userprofile(self, user_id: uuid.UUID) -> UserProfile:
        user_repository = UserRepository(self._session)
        user = await user_repository.eagerly_get_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail='User is not authorized!'
            )

        profile = user.profile
        if profile is None:
            raise HTTPException(
                status_code=404,
                detail='Not found user profile!'
            )

        return profile
