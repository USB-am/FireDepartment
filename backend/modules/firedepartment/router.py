from fastapi import APIRouter, HTTPException

from core.database import TSession
from modules.firedepartment.schemas import FireDepartmentResponse
from modules.firedepartment.service import FireDepartmentService


fd_router = APIRouter(prefix='/firedepartment', tags=['Fire department',])


@fd_router.get('/{firedepartment_id}', response_model=FireDepartmentResponse)
async def get_firedepartment(firedepartment_id: int, session: TSession):
    service = FireDepartmentService(session)
    firedepartment = await service.get_firedepartment(firedepartment_id)

    if firedepartment is None:
        raise HTTPException(
            status_code=404,
            detail='Fire Department is not found!'
        )

    return FireDepartmentResponse.model_validate(firedepartment)
