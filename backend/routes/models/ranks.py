from fastapi import APIRouter, Depends, HTTPException, status
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from auth import TSession
from data_base.schema import RankResponse, CreateRankRequest, UpdateRankRequest
from data_base.session import get_session
from data_base.models import Rank, Human


ranks_router = APIRouter(prefix='/ranks', tags=['Ranks',])


@ranks_router.post('/create', response_model=RankResponse, status_code=status.HTTP_201_CREATED)
async def create_rank(form: CreateRankRequest, session: TSession) -> RankResponse:
    title = form.title
    stmt = select(Rank).filter_by(title=title)
    result = await session.execute(stmt)
    rank = result.scalars().first()

    if rank is not None:
        raise HTTPException(
            status_code=409,
            detail=f'Rank.title=`{title}` is already exists.'
        )

    humans_ids = form.humans_ids
    stmt = select(Human).where(Human.id.in_(humans_ids))
    result = await session.execute(stmt)
    humans = result.scalars().all()

    priority = form.priority
    new_rank = Rank(
        title=title,
        priority=priority,
        humans=humans
    )

    session.add(new_rank)
    await session.commit()

    return RankResponse(
        id=new_rank.id,
        title=new_rank.title,
        priority=new_rank.priority
    )


@ranks_router.put('/update', status_code=status.HTTP_201_CREATED)
async def update_rank(form: UpdateRankRequest, session: TSession) -> None:
    rank_id = form.rank_id
    fields = form.fields

    stmt = update(Rank).where(Rank.id==rank_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


@ranks_router.delete('/delete/{rank_id}', status_code=status.HTTP_200_OK)
async def delete_rank(rank_id: int, session: TSession) -> None:
    stmt = delete(Rank).where(Rank.id==rank_id)
    await session.execute(stmt)
    await session.commit()


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
