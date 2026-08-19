import hashlib
from datetime import timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.config import settings, auth
from core.database import TSession
from core.utils import dt_utcnow
from modules.users.models import User, RefreshToken


class AuthService:
    def __init__(self, session: TSession):
        self._session = session

    async def get_refresh_token_by_token_hash(self, token_hash: str) -> RefreshToken:
        sha_hash = hashlib.sha256(token_hash.encode('utf-8')).hexdigest()
        stmt = (
            select(RefreshToken)
            .where(RefreshToken.token_hash==sha_hash)
            .options(joinedload(RefreshToken.user))
        )
        return await self._session.scalar(stmt)

    async def is_actual_refresh_token(self, refresh_token: RefreshToken) -> bool:
        return dt_utcnow() <= refresh_token.expires_at.replace(tzinfo=timezone.utc) \
            and refresh_token.revoked == False

    async def create_access_token(self, user: User) -> str:
        return auth.create_access_token(uid=str(user.id))

    async def create_refresh_token(self, user: User) -> tuple[str, RefreshToken]:
        refresh_token_value = auth.create_refresh_token(uid=str(user.id))
        sha_hash = hashlib.sha256(refresh_token_value.encode('utf-8')).hexdigest()
        refresh_token = RefreshToken(
            user_id=user.id,
            token_hash=sha_hash,
            expires_at=dt_utcnow() + timedelta(seconds=settings.REFRESH_TOKEN_MAX_AGE),
            revoked=False)

        self._session.add(refresh_token)
        return (refresh_token_value, refresh_token)

    async def revoked_refresh_token(self, refresh_token: RefreshToken) -> None:
        refresh_token.revoked = True
        refresh_token.revoked_at = dt_utcnow()
