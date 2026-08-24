from fastapi import APIRouter

from core.database import TSession
from modules.firedepartment.schemas import FireDepartmentResponse
from modules.firedepartment.service import FireDepartmentService


fd_router = APIRouter(prefix='/firedepartment', tags=['Fire department',])


@fd_router.get('/{fd_id}', response_model=FireDepartmentResponse)
async def get_firedepartment(fd_id: int, session: TSession):
    service = FireDepartmentService(session)
