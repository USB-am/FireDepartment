from fastapi import APIRouter, HTTPException

from core.database import TSession
from core.dependencies import TCurrentUser, RequireRole
from core.security import Role
from modules.firedepartment.schemas import (
    FireDepartmentResponse, CreateFireDepartmentRequest,
    UpdateFireDepartmentRequest)
from modules.firedepartment.service import FireDepartmentService
from modules.users.models import User
from modules.utils.exceptions import DBPrimaryKeyError


fd_router = APIRouter(prefix='/firedepartment', tags=['Fire department',])


@fd_router.get('/{firedepartment_id}', response_model=FireDepartmentResponse)
async def get_firedepartment(
    firedepartment_id: int,
    # user: TCurrentUser,
    session: TSession,
    user: User = RequireRole(Role.dispatch, Role.manager, Role.admin)
):

    service = FireDepartmentService(session)
    firedepartment = await service.get_firedepartment(firedepartment_id)

    if firedepartment is None:
        raise HTTPException(
            status_code=404,
            detail='Fire Department is not found!'
        )

    return FireDepartmentResponse.model_validate(firedepartment)


@fd_router.post('/create', response_model=FireDepartmentResponse)
async def create_firedepartment(
    payload: CreateFireDepartmentRequest,
    user: TCurrentUser,
    session: TSession
):

    service = FireDepartmentService(session)
    try:
        new_firedepartment = await service.create_firedepartment(payload)
    except DBPrimaryKeyError:
        raise HTTPException(
            status_code=409,
            detail=f'FireDepartment.title="{payload.title}" is already exists!'
        )

    return FireDepartmentResponse.model_validate(new_firedepartment)


@fd_router.patch('/update', response_model=FireDepartmentResponse)
async def update_firedepartment(
    payload: UpdateFireDepartmentRequest,
    user: TCurrentUser,
    session: TSession
):

    service = FireDepartmentService(session)
    updated_firedepartment = await service.update_firedepartment(payload)
    return FireDepartmentResponse.model_validate(updated_firedepartment)
