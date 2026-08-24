import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from core.utils import dt_utcnow


if TYPE_CHECKING:
    from modules.auth.models import RefreshToken
    from modules.firedepartment.models import FireDepartment


class User(Base):
    ''' Пользователи '''

    __tablename__ = 'user'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=dt_utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=dt_utcnow,
        onupdate=dt_utcnow)
    refresh_tokens: Mapped[List['RefreshToken']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan')
    profile: Mapped[Optional['UserProfile']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan')

    def __str__(self):
        return self.username


class UserProfile(Base):
    ''' Профиль Пользователя '''

    __tablename__ = 'user_profile'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'),
        unique=True,
        nullable=False)
    call_sign: Mapped[Optional[str]]
    firedepartment_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('fire_department.id', ondelete='SET NULL'))

    firedepartment: Mapped[Optional['FireDepartment']] = relationship(back_populates='profiles')
    user: Mapped['User'] = relationship(back_populates='profile')
