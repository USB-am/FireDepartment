import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from core.database import TSession
from models.user import User
from schemas.user import UserResponse


users_router = APIRouter(prefix='/users', tags=['Users',])


@users_router.get('/all', response_model=list[UserResponse])
async def get_all_users(session: TSession):
    result = await session.scalars(select(User))
    return result.all()


@users_router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: int, session: TSession):
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
