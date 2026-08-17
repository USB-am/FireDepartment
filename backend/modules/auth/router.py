import bcrypt
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from core.database import TSession
from modules.users.schemas import UserResponse
from modules.users.models import User
from modules.users.service import UserService
from modules.auth.service import AuthService
from modules.auth.schemas import UserLoginRequest


auth_router = APIRouter(prefix='/auth', tags=['Auth',])


@auth_router.post('/login', response_model=UserResponse)
async def login_user(login_form: UserLoginRequest, session: TSession):
    user_service = UserService(session)
    user = await user_service.check_login(
        email=login_form.email,
        password=login_form.password)

    auth_service = AuthService(session)
    access_token = await auth_service.create_access_token(user)
    refresh_token = await auth_service.create_refresh_token(user)

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        access_token=access_token,
        refresh_token=refresh_token
    )
