from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.schema import UserResponse, UserAuthResponse, LoginUser
from data_base.session import get_session
from data_base.models import User, SecretKeyUser


users_router = APIRouter(prefix='/users', tags=['Users',])


TSession = Annotated[AsyncSession, Depends(get_session)]


@users_router.get('/{user_id}', response_model=UserResponse)
async def get_user(user_id: int, session: TSession) -> UserResponse:
    stmt = select(User).filter_by(id=user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username
    )


@users_router.post('/auth', response_model=UserAuthResponse)
async def auth_user(form: LoginUser, session: TSession) -> UserAuthResponse:
    email = form.email
    password = form.password

    stmt = select(User).filter_by(email=email)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=422,
            detail='Invalid `email` or `password` fields.'
        )

    stmt = select(SecretKeyUser).filter_by(user_id=user.id)
    result = await session.execute(stmt)
    secret_key = result.scalars().first()

    return UserAuthResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        token=secret_key.secret_key
    )
