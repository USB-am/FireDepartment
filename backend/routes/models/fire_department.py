from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import update, delete

from auth import TSession
from data_base.models import FireDepartment, User
from data_base.schema import (
    FireDepartmentResponse,
    CreateFireDepartmentRequest,
    UpdateFireDepartmentRequest
)


fd_router = APIRouter(prefix='/firedepartments', tags=['Fire departments',])


@fd_router.post('/create', response_model=FireDepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_fire_department(form: CreateFireDepartmentRequest, session: TSession) -> FireDepartmentResponse:
    title = form.title
    stmt = select(FireDepartment).filter_by(title=title)
    result = await session.execute(stmt)
    firedepartment = result.scalars().first()

    if firedepartment is not None:
        raise HTTPException(
            status_code=409,
            detail=f'FireDepartment.title=`{title}` is already exists.'
        )

    users_ids = form.users_ids
    stmt = select(User).where(User.id.in_(users_ids))
    result = await session.execute(stmt)
    users = result.scalars().all()

    new_firedepartment = FireDepartment(
        title=title,
        address=form.address,
        users=users
    )
    session.add(new_firedepartment)
    await session.commit()

    return FireDepartmentResponse(
        id=new_firedepartment.id,
        title=new_firedepartment.title,
        address=new_firedepartment.address
    )


@fd_router.put('/update/{firedepartment_id}', status_code=status.HTTP_201_CREATED)
async def update_firedepartment(form: UpdateFireDepartmentRequest, session: TSession) -> None:
    firedepartment_id = form.firedepartment_id
    fields = form.fields

    stmt = update(FireDepartment).where(FireDepartment.id==firedepartment_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


@fd_router.delete('/delete/{firedepartment_id}', status_code=status.HTTP_200_OK)
async def delete_firedepartment(firedepartment_id: int, session: TSession) -> None:
    stmt = delete(FireDepartment).where(FireDepartment.id==firedepartment_id)
    await session.execute(stmt)
    await session.commit()


@fd_router.get('/{firedepartment_id}', response_model=FireDepartmentResponse)
async def get_firedepartment(firedepartment_id: int, session: TSession) -> FireDepartmentResponse:
    stmt = select(FireDepartment).filter_by(id=firedepartment_id)
    result = await session.execute(stmt)
    firedepartment = result.scalars().first()

    if firedepartment is None:
        raise HTTPException(
            status_code=404,
            detail=f'FireDepartment.id={firedepartment_id} is not already exists!'
        )

    return FireDepartmentResponse(
        id=firedepartment.id,
        title=firedepartment.title,
        address=firedepartment.address
    )
