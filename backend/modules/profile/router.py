import uuid

from fastapi import APIRouter, HTTPException

from core.database import TSession
from core.dependencies import TCurrentUser
from modules.profile.schemas import UserProfileResponse
from modules.profile.service import UserProfileService


profile_router = APIRouter(prefix='/profile', tags=['Profiles',])


@profile_router.get('/me', response_model=UserProfileResponse)
async def get_user_profile(user: TCurrentUser, session: TSession):
    service = UserProfileService(session)
    profile = await service.get_userprofile(user.id)

    return UserProfileResponse(
        id=profile.id,
        call_sign=profile.call_sign if profile.call_sign is not None else '',
        firedepartment_id=profile.firedepartment_id
    )


@profile_router.patch('/update', response_model=UserProfileResponse)
async def update_user_profile(user: TCurrentUser,
                              session: TSession,
                              call_sign: str='',
                              firedepartment_id: int | None=None):
    service = UserProfileService(session)

    profile = await service.get_userprofile(user.id)
    profile.call_sign = call_sign
    profile.firedepartment_id = firedepartment_id

    return UserProfileResponse(
        id=profile.id,
        call_sign=profile.call_sign if profile.call_sign is not None else '',
        firedepartment_id=profile.firedepartment_id
    )
