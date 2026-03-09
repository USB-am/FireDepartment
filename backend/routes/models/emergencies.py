from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import update, delete

from auth import TSession
from data_base.schema import EmergencyResponse, CreateEmergencyRequest, UpdateEmergencyRequest
from data_base.models import Base, Emergency, Tag, Human, Short, Calls


emergencies_router = APIRouter(prefix='/emergencies', tags=['Emergency',])


async def get_entries_by_ids(model: Base, ids: List[int], session: TSession) -> List[Base]:
    stmt = select(model).where(model.id.in_(ids))
    result = await session.execute(stmt)
    return result.scalars().all()


@emergencies_router.post('/create', response_model=EmergencyResponse, status_code=status.HTTP_201_CREATED)
async def create_emergency(form: CreateEmergencyRequest, session: TSession) -> EmergencyResponse:
    title = form.title
    stmt = select(Emergency).filter_by(title=title)
    result = await session.execute(stmt)
    emergency = result.scalars().first()

    if emergency is not None:
        raise HTTPException(
            status_code=409,
            detail=f'Emergency.title=`{title}` is already exists.'
        )

    tags = await get_entries_by_ids(Tag, form.tags_ids, session)
    humans = await get_entries_by_ids(Human, form.humans_ids, session)
    shorts = await get_entries_by_ids(Short, form.shorts_ids, session)
    calls = await get_entries_by_ids(Calls, form.calls_ids, session)

    new_emergency = Emergency(
        title=title,
        description=form.description,
        urgent=form.urgent,
        tags=tags,
        humans=humans,
        shorts=shorts,
        calls=calls
    )
    session.add(new_emergency)
    await session.commit()

    return EmergencyResponse(
        id=new_emergency.id,
        title=new_emergency.title,
        description=new_emergency.description,
        urgent=new_emergency.urgent,
    )


@emergencies_router.put('/update/{emergency_id}', status_code=status.HTTP_201_CREATED)
async def update_emergency(form: UpdateEmergencyRequest, session: TSession) -> None:
    emergency_id = form.emergency_id
    fields = form.fields

    stmt = update(Emergency).where(Emergency.id==emergency_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


@emergencies_router.delete('/delete/{emergency_id}', status_code=status.HTTP_200_OK)
async def delete_emergency(emergency_id: int, session: TSession) -> None:
    stmt = delete(Emergency).where(Emergency.id==emergency_id)
    await session.execute(stmt)
    await session.commit()


@emergencies_router.get('/{emergency_id}', response_model=EmergencyResponse)
async def get_emergency(emergency_id: int, session: TSession) -> EmergencyResponse:
    stmt = select(Emergency).filter_by(id=emergency_id)
    result = await session.execute(stmt)
    emergency = result.scalars().first()

    if emergency is None:
        raise HTTPException(
            status_code=404,
            detail=f'Emergency.id={emergency_id} is not already exists!'
        )

    return EmergencyResponse(
        id=emergency.id,
        title=emergency.title,
        description=emergency.description,
        urgent=emergency.urgent,
    )
