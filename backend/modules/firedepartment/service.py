from core.database import TSession
from modules.firedepartment.models import FireDepartment
from modules.firedepartment.repository import FireDepartmentRepository


class FireDepartmentService:
    def __init__(self, session: TSession):
        self._session = session
        self.repository = FireDepartmentRepository(session)

    async def get_firedepartment(self, fd_id: int) -> FireDepartment:
        return await self.repository.get_firedepartment_by_id(fd_id)
