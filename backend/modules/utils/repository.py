import uuid
from typing import Optional

from sqlalchemy import select, inspect

from core.database import Base, TSession


class BaseRepository[TModel: Base, TId: (int, uuid.UUID)]:
    model: type[TModel]

    def __init__(self, session: TSession):
        self.session = session

    @property
    def pk_column(self):
        return inspect(self.model).primary_key[0]

    async def get_by_id(self, row_id: TId) -> Optional[TModel]:
        stmt = select(self.model).where(self.pk_column==row_id)
        return await self.session.scalar(stmt)
