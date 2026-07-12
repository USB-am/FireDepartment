import hashlib
from datetime import datetime, timedelta
from typing import Tuple

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

# TODO: сделать не магические цифры
ACCESS_TOKEN_MAX_AGE = 15*60
REFRESH_TOKEN_MAX_AGE = 7*24*60*60


def set_token_cookies_to_response(access_token: str, refresh_token: str, response: Response) -> Response:
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=SECURE,
        samesite='lax',
        max_age=ACCESS_TOKEN_MAX_AGE)
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=SECURE,
        samesite='lax',
        max_age=REFRESH_TOKEN_MAX_AGE)
    return response


def create_access_token(user_email: str) -> str:
    return auth.create_access_token(uid=user_email)


def create_refresh_token(user: User) -> Tuple[str, RefreshToken]:
    refresh_token_value = auth.create_refresh_token(uid=user.email)
    sha_hash = hashlib.sha256(refresh_token_value.encode('utf-8')).hexdigest()
    refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=sha_hash,
        expires_at=datetime.utcnow() + timedelta(days=7),
        created_at=datetime.utcnow(),
        revoked=False)

    return (refresh_token_value, refresh_token)


@users_router.post('/login', response_model=UserResponse)
async def login_user(form: UserLoginRequest, session: TSession, response: Response) -> UserResponse:
    stmt = select(User).filter_by(email=form.email)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f'User.email="{form.email}" is not already exists!'
        )

    if not bcrypt.checkpw(form.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(user.email)
    plain_refresh, refresh_token = create_refresh_token(user)

    session.add(refresh_token)
    await session.commit()

    response = set_token_cookies_to_response(access_token, plain_refresh, response)
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username)


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
    old_refresh_token = result.scalars().first()

    if old_refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail=f'Not found actual refresh_token.'
        )
    user = old_refresh_token.user

    access_token = create_access_token(user.email)
    plain_refresh, refresh_token = create_refresh_token(user)
    old_refresh_token.revoked = True

    session.add(refresh_token)
    await session.commit()

    response = set_token_cookies_to_response(access_token, plain_refresh, response)
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

    profile = UserProfile(user_id=new_user.id)
    session.add(profile)

    access_token = create_access_token(email)
    plain_refresh, refresh_token = create_refresh_token(new_user)
    session.add(refresh_token)

    await session.commit()

    response = set_token_cookies_to_response(access_token, plain_refresh, response)
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username
    )
