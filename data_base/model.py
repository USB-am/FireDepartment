import datetime

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Text,
    Date,
    DateTime)
from sqlalchemy.orm import relationship

from .session import Base


# ============ #
# === USER === #
# ============ #

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

# ============ #
# === USER === #
# ============ #


# post_tags = Table('emergency_tags',
#     Column('tag_id', Integer, ForeignKey('Tag.id')),
#     Column('emergency_id', Integer, ForeignKey('Emergency.id')),
# )
# post_humans = Table('emergency_humans',
#     Column('human_id', Integer, ForeignKey('Human.id')),
#     Column('emergency_id', Integer, ForeignKey('Emergency.id')),
# )
# post_shorts = Table('emergency_shorts',
#     Column('short_id', Integer, ForeignKey('Short.id')),
#     Column('emergency_id', Integer, ForeignKey('Emergency.id')),
# )


# class Tag(Base):
#     ''' Теги '''

#     icon = 'pound'
#     __tablename__ = 'Tag'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), unique=True, nullable=False)
#     emergencys = relationship('Emergency', secondary=post_tags,
#                               back_populates='tags')

#     def __str__(self):
#         return self.title


# class Short(Base):
#     ''' Хоткей для ввода информации о вызове '''

#     icon = 'text-short'
#     __tablename__ = 'Short'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), nullable=False)
#     explanation = Column(Text(), nullable=True)
#     into_new_line = Column(Boolean(), nullable=False)

#     def __str__(self):
#         return self.title


# class Rank(Base):
#     ''' Звания '''

#     icon = 'chevron-triple-up'
#     __tablename__ = 'Rank'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), unique=True, nullable=False)
#     priority = Column(Integer, nullable=False)
#     humans = relationship('Human', backref='humans_rank', lazy=True)

#     def __str__(self):
#         return self.title


# class Position(Base):
#     ''' Должности '''

#     icon = 'crosshairs-gps'
#     __tablename__ = 'Position'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), unique=True, nullable=False)
#     humans = relationship('Human', backref='humans_position', lazy=True)

#     def __str__(self):
#         return self.title


# class Human(Base):
#     ''' Люди '''

#     icon = 'account-group'
#     __tablename__ = 'Human'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), nullable=False)
#     phone_1 = Column(String(255), nullable=True)
#     phone_2 = Column(String(255), nullable=True)
#     is_firefigher = Column(Boolean(), nullable=False)
#     work_day = Column(Date(), nullable=True)
#     start_vacation = Column(Date(), nullable=True)
#     finish_vacation = Column(Date(), nullable=True)
#     worktype = Column(Integer, ForeignKey('Worktype.id'), nullable=True)
#     position = Column(Integer, ForeignKey('Position.id'), nullable=True)
#     rank = Column(Integer, ForeignKey('Rank.id'), nullable=True)

#     def is_vacation(self, date: datetime.date) -> bool:
#         ''' Сейчас в отпуске? '''

#         if None in (self.start_vacation, self.finish_vacation):
#             return False

#         return self.start_vacation <= date <= self.finish_vacation

#     def __str__(self):
#         return self.title


# class Emergency(Base):
#     ''' Вызовы '''

#     icon = 'fire-alert'
#     __tablename__ = 'Emergency'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), nullable=False)
#     description = Column(Text(), nullable=True)
#     urgent = Column(Boolean(), nullable=True)
#     tags = relationship('Tag', secondary=post_tags, back_populates='emergencys')
#     humans = relationship('Human', secondary=post_humans, backref='emergencys')
#     shorts = relationship('Short', secondary=post_shorts, backref='emergencys')

#     def __str__(self):
#         return self.title


# class ColorTheme(Base):
#     ''' Цветовая схема '''

#     icon = 'palette'
#     __tablename__ = 'ColorTheme'
#     id = Column(Integer, primary_key=True)
#     primary_palette = Column(String(255), nullable=False)
#     accent_palette = Column(String(255), nullable=False)
#     primary_hue = Column(String(255), nullable=False)   # Оттенок
#     theme_style = Column(String(255), nullable=False)   # Light/Dark
#     background_image = Column(Text(), nullable=True)    # Path to file
#     background_color = Column(String(255), nullable=False)


# class Worktype(Base):
#     ''' График работы '''

#     icon = 'timer-sand'
#     __tablename__ = 'Worktype'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), nullable=False)
#     start_work_day = Column(DateTime(), nullable=False)
#     finish_work_day = Column(DateTime(), nullable=False)
#     work_day_range = Column(Integer, nullable=False)
#     week_day_range = Column(Integer, nullable=False)
#     humans = relationship('Human', backref='humans_worktype', lazy=True)

#     def __str__(self):
#         return self.title


# class UserSettings(Base):
#     ''' Пользовательские настройки '''

#     icon = 'account-wrench'
#     __tablename__ = 'UserSettings'
#     id = Column(Integer, primary_key=True)
#     help_mode = Column(Boolean(), nullable=False)
#     language = Column(String(255), nullable=False)


# class Calls(Base):
#     ''' Информация о вызове '''

#     icon = 'firebase'
#     __tablename__ = 'Calls'
#     id = Column(Integer, primary_key=True)
#     start = Column(DateTime(), nullable=False)
#     finish = Column(DateTime(), nullable=True)
#     emergency = Column(Integer, ForeignKey('Emergency.id'), nullable=False)
#     info = Column(Text(), nullable=True)

#     def __str__(self):
#         start = self.start.strftime('%d.%m.%Y %H:%M:%S')
#         finish = self.finish.strftime('%d.%m.%Y %H:%M:%S')
#         return f'[{start}, {finish}] {self.emergency}'
