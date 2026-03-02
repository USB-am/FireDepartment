from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.schema import PositionResponse
from data_base.session import get_session
from data_base.models import Position


positions_router = APIRouter(prefix='/positions', tags=['Positions',])


TSession = Annotated[AsyncSession, Depends(get_session)]


@positions_router.get('/{position_id}', response_model=PositionResponse)
async def get_position(position_id: int, session: TSession) -> PositionResponse:
    stmt = select(Position).filter_by(id=rank_id)
    result = await session.execute(stmt)
    position = result.scalars().first()

    if position is None:
        raise HTTPException(
            status_code=404,
            detail=f'Position.id={position_id} is not already exists!'
        )

    return PositionResponse(
        id=position.id,
        title=position.title
    )
