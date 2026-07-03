import hashlib
from datetime import datetime, timedelta

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select

from auth import Role, RoleChecker, auth, TSession
from data_base.schema import UserResponse, UserAuthResponse, LoginUser, UserRegisterRequest
from data_base.models import User, RefreshToken, UserProfile


users_router = APIRouter(prefix='/users', tags=['Users',])


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
    password = form.password.encode('utf-8')

    stmt = select(User).filter_by(email=email)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=422,
            detail='Invalid `email` field.'
        )

    stmt = select(HashedPassword).filter_by(user_id=user.id)
    result = await session.execute(stmt)
    pwd_hashed = result.scalars().first()

    if not bcrypt.checkpw(password, pwd_hashed.password_hash):
        raise HTTPException(
            status_code=422,
            detail='Invalid `password` field.'
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
    if result.scalars().first():
        raise HTTPException(
            status_code=409,
            detail=f'User.email="{email}" is already exists!'
        )

    hashed = bcrypt.hashpw(form.password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(
        email=email,
        username=form.username,
        password_hash=hashed.decode('utf-8'),
        role=Role.dispatch.value)
    session.add(new_user)
    await session.flush()

    refresh_token_value = auth.create_refresh_token(uid=new_user.email)
    sha_hash = hashlib.sha256(refresh_token_value.encode('utf-8')).digest()
    token_hash = bcrypt.hashpw(sha_hash, bcrypt.gensalt()).decode('utf-8')
    refresh_token = RefreshToken(
        user_id=new_user.id,
        token_hash=token_hash,
        expires_at=datetime.utcnow() + timedelta(days=7),
        created_at=datetime.utcnow(),
        revoked=False)
    session.add(refresh_token)

    profile = UserProfile(user_id=new_user.id)
    session.add(profile)

    await session.commit()

    access_token = auth.create_access_token(uid=new_user.email)

    return UserAuthResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        token=access_token
    )
