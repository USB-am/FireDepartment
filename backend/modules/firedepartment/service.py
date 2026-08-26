from core.database import TSession
from modules.firedepartment.models import FireDepartment
from modules.firedepartment.schemas import CreateFireDepartmentRequest, UpdateFireDepartmentRequest
from modules.firedepartment.repository import FireDepartmentRepository
from modules.utils.exceptions import DBPrimaryKeyError


class FireDepartmentService:
    def __init__(self, session: TSession):
        self._session = session
        self.repository = FireDepartmentRepository(session)

    async def get_firedepartment(self, fd_id: int) -> FireDepartment | None:
        return await self.repository.get_by_id(fd_id)

    async def create_firedepartment(self, schema: CreateFireDepartmentRequest) -> FireDepartment:
        if await self.repository.get_by_column('title', schema.title) is not None:
            raise DBPrimaryKeyError(f'FireDepartment.title={schema.title} is already exists!')

        new_firedepartment = await self.repository.create(**schema.model_dump())
        self._session.add(new_firedepartment)
        await self._session.flush()

        return new_firedepartment

    async def update_firedepartment(self, schema: UpdateFireDepartmentRequest) -> FireDepartment | None:
        return await self.repository.update(**schema.model_dump())
