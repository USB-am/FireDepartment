from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.schema import CallResponse
from data_base.session import get_session
from data_base.models import Calls


calls_router = APIRouter(prefix='/calls', tags=['Calls',])


TSession = Annotated[AsyncSession, Depends(get_session)]


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
