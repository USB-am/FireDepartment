import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.database import Base


class FireDepartment(Base):
    ''' Запись о пожарной части '''

    __tablename__ = 'fire_department'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str] = mapped_column(nullable=False)
    profiles: Mapped[List['UserProfile']] = relationship(back_populates='firedepartment')

    def __str__(self):
        return self.title


class User(Base):
    ''' Пользователи '''

    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)
    refresh_tokens: Mapped[List['RefreshToken']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan')
    profile: Mapped['UserProfile'] = relationship(
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan')

    def __str__(self):
        return self.username


class RefreshToken(Base):
    ''' Refresh-токены для обновления access-токенов '''

    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    token_hash: Mapped[str] = mapped_column(unique=True, nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)
    revoked: Mapped[bool] = mapped_column(default=False)
    revoked_at: Mapped[Optional[datetime.datetime]]

    user: Mapped['User'] = relationship(back_populates='refresh_tokens')

    def __str__(self):
        return f'RefreshToken(user={self.user_id}, expires={self.expires_at})'


class UserProfile(Base):
    ''' Профиль Пользователя '''

    __tablename__ = 'user_profile'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'),
        unique=True,
        nullable=False)
    call_sign: Mapped[Optional[str]]
    firedepartment_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('fire_department.id', ondelete='SET NULL'))

    firedepartment: Mapped[Optional['FireDepartment']] = relationship(back_populates='profiles')
    user: Mapped['User'] = relationship(back_populates='profile')


from sqlalchemy import Index
Index('idx_user_email', User.email)
Index('idx_refresh_token_hash', RefreshToken.token_hash)
Index('idx_refresh_user_id', RefreshToken.user_id)
