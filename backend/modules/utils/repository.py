import uuid
from typing import Any, TYPE_CHECKING

from sqlalchemy import select, update as sql_update, inspect

from core.database import Base, TSession


if TYPE_CHECKING:
    from sqlalchemy.sql.elements import ColumnElement


class BaseRepository[TModel: Base, TId: (int, uuid.UUID)]:
    model: type[TModel]

    def __init__(self, session: TSession):
        self.session = session

    @property
    def pk_column(self) -> 'ColumnElement[Any]':
        return inspect(self.model).primary_key[0]

    async def get_by_id(self, row_id: TId) -> TModel | None:
        stmt = select(self.model).where(self.pk_column==row_id)
        return await self.session.scalar(stmt)

    async def get_by_column(self, column_name: str, value: Any) -> TModel | None:
        stmt = select(self.model).where(getattr(self.model, column_name)==value)
        return await self.session.scalar(stmt)

    async def create(self, **fields) -> TModel:
        return self.model(**fields)

    async def update(self, **fields) -> TModel | None:
        field_id = fields.pop('id', None)
        if field_id is None:
            raise ValueError

        stmt = sql_update(self.model)\
            .where(self.pk_column==field_id)\
            .values(**fields)\
            .returning(self.model)
        return await self.session.scalar(stmt)
