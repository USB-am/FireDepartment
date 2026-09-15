import uuid

from fastapi import APIRouter, HTTPException

from core.database import TSession
from core.dependencies import TCurrentUser
from modules.profile.schemas import UserProfileResponse
from modules.users.repository import UserRepository


profile_router = APIRouter(prefix='/profile', tags=['Profiles',])


@profile_router.get('/me', response_model=UserProfileResponse)
async def get_user_profile(user: TCurrentUser, session: TSession):
    repo = UserRepository(session)
    eagerly_user = await repo.eagerly_get_user(user.id)
    if eagerly_user is None:
        raise HTTPException(
            status_code=401,
            detail='Not found profile!'
        )

    profile = eagerly_user.profile

    if profile is None:
        raise HTTPException(
            status_code=401,
            detail='Not found profile!'
        )

    return UserProfileResponse(
        id=profile.id,
        call_sign=profile.call_sign if profile.call_sign is not None else '',
        firedepartment_id=profile.firedepartment_id
    )
