from fastapi import APIRouter, Depends, HTTPException, status
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from data_base.schema import PositionResponse, CreatePositionRequest, UpdatePositionRequest
from data_base.session import get_session
from data_base.models import Position, Human


positions_router = APIRouter(prefix='/positions', tags=['Positions',])


TSession = Annotated[AsyncSession, Depends(get_session)]


@positions_router.post('/create', response_model=PositionResponse, status_code=status.HTTP_201_CREATED)
async def create_position(form: CreatePositionRequest, session: TSession) -> PositionResponse:
    title = form.title

    stmt = select(Position).filter_by(title=title)
    result = await session.execute(stmt)
    position = result.scalars().first()

    if position is not None:
        raise HTTPException(
            status_code=409,
            detail=f'Position.title=`{title}` is already exists.'
        )

    humans_ids = form.humans_ids
    stmt = select(Human).where(Human.id.in_(humans_ids))
    result = await session.execute(stmt)
    humans = result.scalars().all()

    new_position = Position(
        title=title,
        humans=humans
    )

    session.add(new_position)
    await session.commit()

    return PositionResponse(
        id=new_position.id,
        title=new_position.title
    )


@positions_router.put('/update/{position_id}', status_code=status.HTTP_201_CREATED)
async def update_position(form: UpdatePositionRequest, session: TSession) -> None:
    position_id = form.position_id
    fields = form.fields

    stmt = update(Position).where(Position.id==position_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


@positions_router.delete('/delete/{position_id}', status_code=status.HTTP_200_OK)
async def delete_position(position_id: int, session: TSession) -> None:
    stmt = delete(Position).where(Position.id==position_id)
    await session.execute(stmt)
    await session.commit()


@positions_router.get('/{position_id}', response_model=PositionResponse)
async def get_position(position_id: int, session: TSession) -> PositionResponse:
    stmt = select(Position).filter_by(id=position_id)
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
