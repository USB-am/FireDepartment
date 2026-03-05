from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import update, delete

from auth import TSession
from data_base.schema import (
    ShortResponse,
    CreateShortRequest,
    UpdateShortRequest)
from data_base.session import get_session
from data_base.models import Short, Emergency


shorts_router = APIRouter(prefix='/shorts', tags=['Shorts',])


@shorts_router.post('/create', response_model=ShortResponse, status_code=status.HTTP_201_CREATED)
async def create_short(form: CreateShortRequest, session: TSession) -> ShortResponse:
    title = form.title
    stmt = select(Short).filter_by(title=title)
    result = await session.execute(stmt)
    short = result.scalars().first()

    if short is not None:
        raise HTTPException(
            status_code=409,
            detail=f'Short.title=`{title}` is already exists.'
        )

    emergencies_ids = form.emergencies_ids
    stmt = select(Emergency).where(Emergency.id.in_(emergencies_ids))
    result = await session.execute(stmt)
    emergencies = result.scalars().all()

    explanation = form.explanation
    into_new_line = form.into_new_line

    new_short = Short(
        title=title,
        explanation=explanation if explanation else title,
        into_new_line=into_new_line,
        emergencies=emergencies
    )
    session.add(new_short)
    await session.commit()

    return ShortResponse(
        id=new_short.id,
        title=new_short.title,
        explanation=new_short.explanation,
        into_new_line=new_short.into_new_line,
    )


@shorts_router.put('/update/{short_id}', status_code=status.HTTP_201_CREATED)
async def update_short(form: UpdateShortRequest, session: TSession) -> None:
    short_id = form.short_id
    fields = form.fields

    stmt = update(Short).where(Short.id==short_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


@shorts_router.delete('/delete/{short_id}', status_code=status.HTTP_200_OK)
async def delete_short(short_id: int, session: TSession) -> None:
    stmt = delete(Short).where(Short.id==short_id)
    await session.execute(stmt)
    await session.commit()


@shorts_router.get('/{short_id}', response_model=ShortResponse)
async def get_short(short_id: int, session: TSession) -> ShortResponse:
    stmt = select(Short).filter_by(id=short_id)
    result = await session.execute(stmt)
    short = result.scalars().first()

    if short is None:
        raise HTTPException(
            status_code=404,
            detail=f'Short.id={short_id} is not already exists!'
        )

    return ShortResponse(
        id=short.id,
        title=short.title,
        explanation=short.explanation,
        into_new_line=short.into_new_line
    )