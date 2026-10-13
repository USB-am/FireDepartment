import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


if TYPE_CHECKING:
    from modules.firedepartment.models import FireDepartment


class Employee(Base):
    ''' Запись о Сотруднике '''

    __tablename__ = 'employee'
    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4)
    surname: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str] = mapped_column(nullable=False)

    firedepartment_id: Mapped[int] = mapped_column(
        ForeignKey('fire_department.id', ondelete='SET NULL'))
    firedepartment: Mapped['FireDepartment'] = relationship(back_populates='employees')

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'
