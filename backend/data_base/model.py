import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .session import Base


# ============ #
# === USER === #

class User(Base):
    ''' Пользователи '''

    __tablename__ = 'User'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    fd_number: Mapped[Optional[int]]
    # secret_key: Mapped[Optional[str]] = mapped_column(unique=True)
    created_at: Mapped[Optional[str]]
    last_used: Mapped[Optional[str]]

    def __str__(self):
        return self.username


class SecretKeyUser(Base):
    ''' Связь SecretKey для User '''

    __tablename__ = 'SecretKey'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))
    secret_key: Mapped[str] = mapped_column(unique=True)

# === USER === #
# ============ #

# ======================= #
# === FRONTEND MODELS === #


tags_emergencies = Table(
    'tags_emergencies',
    Base.metadata,
    Column('tag', ForeignKey('Tag.id'), primary_key=True),
    Column('emergency', ForeignKey('Emergency.id'), primary_key=True),
)

humans_emergencies = Table(
    'humans_emergencies',
    Base.metadata,
    Column('human', ForeignKey('Human.id'), primary_key=True),
    Column('emergency', ForeignKey('Emergency.id'), primary_key=True),
)

shorts_emergencies = Table(
    'shorts_emergencies',
    Base.metadata,
    Column('short', ForeignKey('Short.id'), primary_key=True),
    Column('emergency', ForeignKey('Emergency.id'), primary_key=True),
)


class Tag(Base):
    ''' Теги '''

    icon = 'pound'
    __tablename__ = 'Tag'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    emergencies: Mapped[List['Emergency']] = relationship(secondary=tags_emergencies,
                                                          back_populates='tags')

    def __str__(self):
        return self.title


class Short(Base):
    ''' Хоткей для ввода информации о вызове '''

    icon = 'text-short'
    __tablename__ = 'Short'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    explanation: Mapped[Optional[str]]
    into_new_line: Mapped[bool]
    emergencies: Mapped[List['Emergency']] = relationship(secondary=shorts_emergencies,
                                                          back_populates='shorts')

    def __str__(self):
        return self.title


class Rank(Base):
    ''' Звания '''

    icon = 'chevron-triple-up'
    __tablename__ = 'Rank'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    priority: Mapped[int]
    humans: Mapped[List['Human']] = relationship(back_populates='rank')

    def __str__(self):
        return self.title


class Position(Base):
    ''' Должности '''

    icon = 'crosshairs-gps'
    __tablename__ = 'Position'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    humans: Mapped[List['Human']] = relationship(back_populates='position')

    def __str__(self):
        return self.title


class Human(Base):
    ''' Люди '''

    icon = 'account-group'
    __tablename__ = 'Human'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    phone_1: Mapped[Optional[str]]
    phone_2: Mapped[Optional[str]]
    is_firefigher: Mapped[bool]
    work_day: Mapped[datetime.date]
    start_vacation: Mapped[datetime.date]
    finish_vacation: Mapped[datetime.date]
    worktype_id: Mapped[int] = mapped_column(ForeignKey('Worktype.id'))
    position_id: Mapped[int] = mapped_column(ForeignKey('Position.id'))
    rank_id: Mapped[int] = mapped_column(ForeignKey('Rank.id'))
    worktype: Mapped['Worktype'] = relationship(back_populates='humans')
    position: Mapped['Position'] = relationship(back_populates='humans')
    rank: Mapped['Rank'] = relationship(back_populates='humans')
    emergencies: Mapped[List['Emergency']] = relationship(secondary=humans_emergencies,
                                                          back_populates='humans')

    def is_vacation(self, date: datetime.date) -> bool:
        ''' Сейчас в отпуске? '''

        if None in (self.start_vacation, self.finish_vacation):
            return False

        return self.start_vacation <= date <= self.finish_vacation

    def __str__(self):
        return self.title


class Emergency(Base):
    ''' Вызовы '''

    icon = 'fire-alert'
    __tablename__ = 'Emergency'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    urgent: Mapped[bool]
    tags: Mapped[List['Tag']] = relationship(secondary=tags_emergencies,
                                             back_populates='emergencies')
    humans: Mapped[List['Human']] = relationship(secondary=humans_emergencies,
                                                 back_populates='emergencies')
    shorts: Mapped[List['Short']] = relationship(secondary=shorts_emergencies,
                                                 back_populates='emergencies')
    calls: Mapped[List['Calls']] = relationship(back_populates='emergency')

    def __str__(self):
        return self.title


class ColorTheme(Base):
    ''' Цветовая схема '''

    icon = 'palette'
    __tablename__ = 'ColorTheme'
    id: Mapped[int] = mapped_column(primary_key=True)
    primary_palette: Mapped[str]
    accent_palette: Mapped[str]
    primary_hue: Mapped[str]        # Оттенок
    theme_style: Mapped[str]        # Light/Dark
    background_image: Mapped[str]   # Path to file
    background_color: Mapped[str]


class Worktype(Base):
    ''' График работы '''

    icon = 'timer-sand'
    __tablename__ = 'Worktype'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    start_work_day: Mapped[datetime.datetime]
    finish_work_day: Mapped[datetime.datetime]
    work_day_range: Mapped[int]
    week_day_range: Mapped[int]
    humans: Mapped[List['Human']] = relationship(back_populates='worktype')

    def __str__(self):
        return self.title


class UserSettings(Base):
    ''' Пользовательские настройки '''

    icon = 'account-wrench'
    __tablename__ = 'UserSettings'
    id: Mapped[int] = mapped_column(primary_key=True)
    help_mode: Mapped[bool]
    language: Mapped[str]


class Calls(Base):
    ''' Информация о вызове '''

    icon = 'firebase'
    __tablename__ = 'Calls'
    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[datetime.datetime]
    finish: Mapped[datetime.datetime]
    emergency_id: Mapped[int] = mapped_column(ForeignKey('Emergency.id'))
    emergency: Mapped['Emergency'] = relationship(back_populates='calls')
    info: Mapped[Optional[str]]

    def __str__(self):
        start = self.start.strftime('%d.%m.%Y %H:%M:%S')
        finish = self.finish.strftime('%d.%m.%Y %H:%M:%S')
        return f'[{start}, {finish}] {self.emergency}'

# === FRONTEND MODELS === #
# ======================= #
