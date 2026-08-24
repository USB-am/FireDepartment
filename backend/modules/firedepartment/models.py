from typing import List, TYPE_CHECKING

from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from modules.users.models import UserProfile


class FireDepartment(Base):
    ''' Запись о пожарной части '''

    __tablename__ = 'fire_department'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str] = mapped_column(nullable=False)
    profiles: Mapped[List['UserProfile']] = relationship(back_populates='firedepartment')

    def __str__(self):
        return self.title
