import uuid
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from core.database import Base
from core.utils import dt_utcnow
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from modules.users.models import User


class RefreshToken(Base):
    ''' Refresh-токены для обновления access-токенов '''

    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    token_hash: Mapped[str] = mapped_column(unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=dt_utcnow)
    revoked: Mapped[bool] = mapped_column(default=False)
    revoked_at: Mapped[Optional[datetime]]

    user: Mapped['User'] = relationship(back_populates='refresh_tokens')

    def __str__(self):
        return f'RefreshToken(user={self.user_id}, expires={self.expires_at})'


Index('idx_refresh_user_id', RefreshToken.user_id)
