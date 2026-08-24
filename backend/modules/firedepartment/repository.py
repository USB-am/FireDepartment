from sqlalchemy import select

from core.database import TSession
from modules.firedepartment.models import FireDepartment


class FireDepartmentRepository:
    def __init__(self, session: TSession):
        self._session = session

    async def get_firedepartment_by_id(self, fd_id: int) -> FireDepartment:
        stmt = select(FireDepartment).where(FireDepartment.id==fd_id)
        return await self._session.scalar(stmt)
