import uuid
from typing import Annotated, Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from authx import RequestToken

from core.database import TSession
from core.security import Role
from core.config import auth
from modules.users.service import UserService
from modules.users.models import User


security = HTTPBearer()


async def get_current_user(
        session: TSession,
        credentials: HTTPAuthorizationCredentials=Depends(security)
) -> User:
    try:
        token_string = credentials.credentials
        token = RequestToken(token=token_string, location='headers')
        payload = auth.verify_token(token, verify_csrf=False)
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


class RoleChecker:
    def __init__(self, *allowed_roles: Role):
        self.allowed_roles = [r.value for r in allowed_roles]

    async def __call__(self, user: User = Depends(get_current_user)) -> User:
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail='You don\'t have permission to access this resource!'
            )
        return user


def RequireRole(*roles: Role) -> Any:
    return Depends(RoleChecker(*roles))
