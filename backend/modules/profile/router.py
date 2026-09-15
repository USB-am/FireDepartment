import uuid

from fastapi import APIRouter, HTTPException

from core.database import TSession
from core.dependencies import TCurrentUser
from modules.profile.schemas import UserProfileResponse
from modules.profile.service import UserProfileSerice


profile_router = APIRouter(prefix='/profile', tags=['Profiles',])


@profile_router.get('/me', response_model=UserProfileResponse)
async def get_user_profile(user: TCurrentUser, session: TSession):
    service = UserProfileSerice(session)
    profile = await service.get_userprofile(user.id)

    return UserProfileResponse(
        id=profile.id,
        call_sign=profile.call_sign if profile.call_sign is not None else '',
        firedepartment_id=profile.firedepartment_id
    )
