from datetime import datetime

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth import Role, RoleChecker, auth
from data_base.schema import UserResponse, UserAuthResponse, LoginUser, UserRegisterRequest
from data_base.session import get_session
from data_base.models import User, SecretKeyUser, HashedPassword


users_router = APIRouter(prefix='/users', tags=['Users',])
TSession = Annotated[AsyncSession, Depends(get_session)]


@users_router.get(
    '/{user_id}',
    response_model=UserResponse,
    dependencies=[Depends(
        RoleChecker([
            Role.admin,
            Role.manager,
            Role.dispatch,
            Role.reader
        ]))
    ])
async def get_user(user_id: int, session: TSession) -> UserResponse:
    stmt = select(User).filter_by(id=user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f'User.id={user_id} is not already exists!'
        )

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


@users_router.post('/register', response_model=UserAuthResponse)
async def create_user(form: UserRegisterRequest, session: TSession) -> UserAuthResponse:
    email = form.email

    stmt = select(User).filter_by(email=email)
    result = await session.execute(stmt)
    found_user = result.scalars().first()

    if found_user:
        raise HTTPException(
            status_code=409,
            detail=f'User.email={email} is already exists!'
        )

    username = form.username
    pwd = form.password

    created_at = datetime.now().isoformat()

    new_user = User(
        email=email,
        username=username,
        role=Role.dispatch.value,
        created_at=created_at,
        last_used=created_at)
    session.add(new_user)
    await session.commit()

    session.add(HashedPassword(
        user_id=new_user.id,
        password_hash=bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
    ))
    secret_key = SecretKeyUser(
        user_id=new_user.id,
        secret_key=auth.create_access_token(uid=email)
    )
    session.add(secret_key)
    await session.commit()

    return UserAuthResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        token=secret_key.secret_key
    )
