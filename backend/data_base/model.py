from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey)

from .session import Base


# ============ #
# === USER === #

class User(Base):
    ''' Пользователи '''

    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    secret_key = Column(String(255), unique=True, nullable=False)
    created_at = Column(String(255), nullable=False)
    last_used = Column(String(255), nullable=True)

    def __str__(self):
        return self.username


class SecretKeyUser(Base):
    ''' Связь SecretKey для User '''

    __tablename__ = 'SecretKey'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False, unique=True)
    secret_key = Column(String(255), unique=True, nullable=False)

# === USER === #
# ============ #
