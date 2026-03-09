from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import update, delete

from auth import TSession
from data_base.schema import CallResponse, CreateCallRequest, UpdateCallRequest
from data_base.models import Calls, Emergency


calls_router = APIRouter(prefix='/calls', tags=['Calls',])


@calls_router.post('/create', response_model=CallResponse, status_code=status.HTTP_201_CREATED)
async def create_call(form: CreateCallRequest, session: TSession) -> CallResponse:
    emergency_id = form.emergency_id
    stmt = select(Emergency).filter_by(id=emergency_id)
    result = await session.execute(stmt)
    emergency = result.scalars().first()

    new_call = Calls(
        start=form.start,
        finish=form.finish,
        emergency_id=emergency_id,
        emergency=emergency,
        info=form.info
    )
    session.add(new_call)
    await session.commit()

    return CallResponse(
        id=new_call.id,
        start=new_call.start,
        finish=new_call.finish,
        info=new_call.info
    )


@calls_router.put('/update/{call_id}', status_code=status.HTTP_201_CREATED)
async def update_call(form: UpdateCallRequest, session: TSession) -> None:
    call_id = form.call_id
    fields = form.fields

    stmt = update(Calls).where(Calls.id==call_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


@calls_router.delete('/delete/{call_id}', status_code=status.HTTP_200_OK)
async def delete_call(call_id: int, session: TSession) -> None:
    stmt = delete(Calls).where(Calls.id==call_id)
    await session.execute(stmt)
    await session.commit()


@calls_router.get('/{call_id}', response_model=CallResponse)
async def get_call(call_id: int, session: TSession) -> CallResponse:
    stmt = select(Calls).filter_by(id=call_id)
    result = await session.execute(stmt)
    call = result.scalars().first()

    if call is None:
        raise HTTPException(
            status_code=404,
            detail=f'Call.id={call_id} is not already exists!'
        )

    return CallResponse(
        id=call.id,
        start=call.start,
        finish=call.finish,
        info=call.info
    )
