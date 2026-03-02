from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.schema import EmergencyResponse
from data_base.session import get_session
from data_base.models import Emergency


emergencies_router = APIRouter(prefix='/emergencies', tags=['Emergency',])


TSession = Annotated[AsyncSession, Depends(get_session)]


@emergencies_router.get('/{emergency_id}', response_model=EmergencyResponse)
async def get_emergency(emergency_id: int, session: TSession) -> EmergencyResponse:
    stmt = select(Short).filter_by(id=emergency_id)
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
