from fastapi import APIRouter, HTTPException

from core.database import TSession
from modules.users.schemas import UserResponse, TokensResponse
from modules.users.service import UserService
from modules.auth.service import AuthService
from modules.auth.schemas import UserLoginRequest, UserRegisterRequest, RefreshTokenRequest


auth_router = APIRouter(prefix='/auth', tags=['Auth',])


@auth_router.post('/refresh', response_model=TokensResponse)
async def refresh_tokens(refresh_request: RefreshTokenRequest, session: TSession):
    refresh_token_hash = refresh_request.refresh_token

    auth_service = AuthService(session)
    refresh_token = await auth_service.get_refresh_token_by_token_hash(refresh_token_hash)
    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail='Unauthorized error! 1'
        )

    if not await auth_service.is_actual_refresh_token(refresh_token):
        raise HTTPException(
            status_code=401,
            detail='Unauthorized error! 2'
        )
    await auth_service.revoked_refresh_token(refresh_token)

    current_user = refresh_token.user
    access_token_value = await auth_service.create_access_token(user=current_user)
    refresh_token_value, _ = await auth_service.create_refresh_token(user=current_user)

    return TokensResponse(
        access_token=access_token_value,
        refresh_token=refresh_token_value
    )


@auth_router.post('/login', response_model=UserResponse)
async def login_user(login_form: UserLoginRequest, session: TSession):
    user_service = UserService(session)
    user = await user_service.check_login(
        email=login_form.email,
        password=login_form.password)

    auth_service = AuthService(session)
    access_token_value = await auth_service.create_access_token(user)
    refresh_token_value, _ = await auth_service.create_refresh_token(user)

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        access_token=access_token_value,
        refresh_token=refresh_token_value
    )


@auth_router.post('/register', response_model=UserResponse)
async def register_user(register_form: UserRegisterRequest, session: TSession):
    user_service = UserService(session)
    if await user_service.user_is_exists(register_form.email):
        raise HTTPException(
            status_code=409,
            detail='User with this email already exists.'
        )

    user = await user_service.create_user(**register_form.model_dump())
    await session.flush()

    await user_service.create_user_profile(user)

    auth_service = AuthService(session)
    access_token_value = await auth_service.create_access_token(user)
    refresh_token_value, _ = await auth_service.create_refresh_token(user)

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        access_token=access_token_value,
        refresh_token=refresh_token_value
    )
