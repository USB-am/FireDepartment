import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from authx import RequestToken

from core.database import TSession
from core.config import auth
from modules.users.service import UserService
from modules.users.models import User

auth.get_access_token_from_request

async def get_current_user(token: RequestToken, session: TSession) -> User:
    try:
        payload = auth.verify_token(token)
        user_id = payload.sub
    except Exception:
        raise HTTPException(
            status_code=401,
            detail='Invalid or expired access token!'
        )

    user_service = UserService(session)
    user = await user_service.repository.get_user(user_id=uuid.UUID(user_id))
    if user is None:
        raise HTTPException(
            status_code=401,
            detail='User not found!'
        )
    return user


TCurrentUser = Annotated[User, Depends(get_current_user)]
