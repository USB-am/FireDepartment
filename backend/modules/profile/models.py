import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


if TYPE_CHECKING:
    from modules.users.models import User
    from modules.firedepartment.models import FireDepartment


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

