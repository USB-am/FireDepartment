import hashlib
from datetime import datetime, timedelta

import bcrypt
from fastapi import APIRouter, HTTPException, Request, Response
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from core.database import TSession
from core.config import auth, SECURE
from core.security import Role, RoleChecker
from schemas.user import UserRegisterRequest, UserLoginRequest, UserResponse
from models.user import User, RefreshToken, UserProfile


users_router = APIRouter(prefix='/users', tags=['Users',])


@users_router.post('/login', response_model=UserResponse)
async def login_user(form: UserLoginRequest, session: TSession, response: Response) -> UserResponse:
    stmt = select(User).filter_by(email=form.email)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f'User.email="{email}" is not already exists!'
        )


@users_router.post('/refresh')
async def refresh_access(request: Request, session: TSession, response: Response) -> dict:
    user_refresh_token = request.cookies.get('refresh_token')
    if user_refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail=f'refresh_token is not found!'
        )

    incoming_hash = hashlib.sha256(user_refresh_token.encode('utf-8')).hexdigest()
    stmt = select(RefreshToken).options(selectinload(RefreshToken.user)).filter(
        RefreshToken.token_hash==incoming_hash,
        RefreshToken.revoked==False,
        RefreshToken.expires_at>datetime.utcnow())
    result = await session.execute(stmt)
    refresh_token = result.scalars().first()

    user = refresh_token.user

    access_token = auth.create_access_token(uid=user.email)
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=SECURE,
        samesite='lax',
        max_age=15*60)

    refresh_token_value = auth.create_refresh_token(uid=user.email)
    sha_hash = hashlib.sha256(refresh_token_value.encode('utf-8')).hexdigest()
    refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=sha_hash,
        expires_at=datetime.utcnow() + timedelta(days=7),
        created_at=datetime.utcnow(),
        revoked=False)
    session.add(refresh_token)
    await session.commit()

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=SECURE,
        samesite='lax',
        max_age=7*24*60*60)

    return {'status_code': 200, 'detail': 'Access-token is updated.'}


@users_router.post('/register', response_model=UserResponse)
async def create_user(form: UserRegisterRequest, session: TSession, response: Response) -> UserResponse:
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
    # sha_hash = hashlib.sha256(refresh_token_value.encode('utf-8')).digest()
    sha_hash = hashlib.sha256(refresh_token_value.encode('utf-8')).hexdigest()
    # token_hash = bcrypt.hashpw(sha_hash, bcrypt.gensalt()).decode('utf-8')
    refresh_token = RefreshToken(
        user_id=new_user.id,
        token_hash=sha_hash,
        expires_at=datetime.utcnow() + timedelta(days=7),
        created_at=datetime.utcnow(),
        revoked=False)
    session.add(refresh_token)

    profile = UserProfile(user_id=new_user.id)
    session.add(profile)

    await session.commit()

    access_token = auth.create_access_token(uid=new_user.email)

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=SECURE,
        samesite='lax',
        max_age=15*60)  # TODO: сделать не магические цифры
    response.set_cookie(
        key='refresh_token',
        value=refresh_token_value,
        httponly=True,
        secure=SECURE,
        samesite='lax',
        max_age=7*24*60*60)  # TODO: сделать не магические цифры

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username
    )
