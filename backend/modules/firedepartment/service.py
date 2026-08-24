from typing import Optional

from core.database import TSession
from modules.firedepartment.models import FireDepartment
from modules.firedepartment.repository import FireDepartmentRepository


class FireDepartmentService:
    def __init__(self, session: TSession):
        self._session = session
        self.repository = FireDepartmentRepository(session)

    async def get_firedepartment(self, fd_id: int) -> Optional[FireDepartment]:
        return await self.repository.get_by_id(fd_id)
