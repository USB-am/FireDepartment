import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from core.database import TSession
from core.dependencies import TCurrentUser
from modules.users.models import User
from modules.users.schemas import ShortUserResponse, UserResponse


users_router = APIRouter(prefix='/users', tags=['Users',])


@users_router.get('/me', response_model=ShortUserResponse)
async def get_me(user: TCurrentUser):
    return ShortUserResponse(
        id=user.id,
        email=user.email,
        username=user.username
    )


@users_router.get('/all', response_model=list[UserResponse])
async def get_all_users(session: TSession):
    result = await session.scalars(select(User))
    _response: list[UserResponse] = []
    for user in result.all():
        refresh_tokens = user.refresh_tokens
        filtered_r_tokens = list(filter(lambda t: t.revoked==False, refresh_tokens))
        refresh_token = filtered_r_tokens[0]
        _response.append(
            UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                access_token='wqe',
                refresh_token=refresh_token
            )
        )
    return _response


@users_router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: uuid.UUID, session: TSession):
    stmt = select(User).filter_by(id=user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail=f'User.id={user_id} not found!')

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        access_token='qwe',
        refresh_token='asd'
    )
