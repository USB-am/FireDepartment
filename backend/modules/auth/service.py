import hashlib
from datetime import timedelta
from typing import Optional

from sqlalchemy import select

from core.config import settings, auth
from core.database import TSession
from core.utils import dt_utcnow
from modules.users.models import User, RefreshToken


class AuthService:
    def __init__(self, session: TSession):
        self._session = session
    
    async def create_access_token(self, user: User) -> str:
        return auth.create_access_token(uid=user.id)

    async def create_refresh_token(self, user: User) -> tuple[str, RefreshToken]:
        await self.revoked_refresh_token(user)

        refresh_token_value = auth.create_refresh_token(user.id)
        sha_hash = hashlib.sha256(refresh_token_value.encode('utf-8')).hexdigest()
        refresh_token = RefreshToken(
            user_id=user.id,
            token_hash=sha_hash,
            expires_at=dt_utcnow() + timedelta(seconds=settings.REFRESH_TOKEN_MAX_AGE),
            revoked=False)

        self._session.add(refresh_token)
        return (refresh_token_value, refresh_token)

    async def get_active_refresh_token(self, user: User) -> Optional[RefreshToken]:
        stmt = select(RefreshToken).where(
            RefreshToken.user_id==user.id,
            RefreshToken.revoked==False
        ).limit(1)
        return await self._session.scalar(stmt)

    async def revoked_refresh_token(self, user: User) -> None:
        refresh_token = await self.get_active_refresh_token(user)

        if refresh_token is not None:
            refresh_token.revoked = True
            refresh_token.revoked_at = dt_utcnow()
