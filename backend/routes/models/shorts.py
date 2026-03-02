from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.schema import ShortResponse
from data_base.session import get_session
from data_base.models import Short


shorts_router = APIRouter(prefix='/shorts', tags=['Shorts',])


TSession = Annotated[AsyncSession, Depends(get_session)]


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