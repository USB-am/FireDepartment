from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.schema import RankResponse
from data_base.session import get_session
from data_base.models import Rank


ranks_router = APIRouter(prefix='/ranks', tags=['Ranks',])


TSession = Annotated[AsyncSession, Depends(get_session)]


@ranks_router.get('/{rank_id}', response_model=RankResponse)
async def get_rank(rank_id: int, session: TSession) -> RankResponse:
    stmt = select(Rank).filter_by(id=rank_id)
    result = await session.execute(stmt)
    rank = result.scalars().first()

    if rank is None:
        raise HTTPException(
            status_code=404,
            detail=f'Rank.id={rank_id} is not already exists!'
        )

    return RankResponse(
        id=rank.id,
        title=rank.title,
        priority=rank.priority
    )
