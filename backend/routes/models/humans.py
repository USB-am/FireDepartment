from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import update, delete

from auth import TSession
from data_base.schema import HumanResponse, CreateHumanRequest, UpdateHumanRequest
from data_base.models import (
    Base,
    Human,
    Rank,
    Position,
    Worktype,
    Emergency
)


humans_router = APIRouter(prefix='/humans', tags=['Humans',])


async def get_entry_by_id(entry_id: int, model: Base, session: TSession) -> Base:
    stmt = select(model).where(model.id==entry_id)
    result = await session.execute(stmt)
    return result.scalars().first()


@humans_router.post('/create', response_model=HumanResponse, status_code=status.HTTP_201_CREATED)
async def create_human(form: CreateHumanRequest, session: TSession) -> HumanResponse:
    title = form.title
    work_day = datetime.strptime(form.work_day, '%Y-%m-%d')
    start_vacation = datetime.strptime(form.start_vacation, '%Y-%m-%d')
    finish_vacation = datetime.strptime(form.finish_vacation, '%Y-%m-%d')

    rank = await get_entry_by_id(form.rank_id, Rank, session)
    position = await get_entry_by_id(form.position_id, Position, session)
    worktype = await get_entry_by_id(form.worktype_id, Worktype, session)
    stmt = select(Emergency).where(Emergency.id.in_(form.emergencies_ids))
    result = await session.execute(stmt)
    emergencies = result.scalars().all()

    new_human = Human(
        title=title,
        phone_1=form.phone_1,
        phone_2=form.phone_2,
        is_firefigher=form.is_firefigher,
        work_day=work_day,
        start_vacation=start_vacation,
        finish_vacation=finish_vacation,
        worktype_id=worktype.id,
        worktype=worktype,
        position_id=position.id,
        position=position,
        rank_id=rank.id,
        rank=rank,
        emergencies=emergencies,
    )
    session.add(new_human)
    await session.commit()

    return HumanResponse(
        id=new_human.id,
        title=new_human.title,
        phone_1=new_human.phone_1,
        phone_2=new_human.phone_2,
        is_firefigher=new_human.is_firefigher,
    )


@humans_router.put('/update/{human_id}', status_code=status.HTTP_201_CREATED)
async def update_human(form: UpdateHumanRequest, session: TSession) -> None:
    human_id = form.human_id
    fields = form.fields
    stmt = update(Human).where(Human.id==human_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


@humans_router.delete('/delete/{human_id}', status_code=status.HTTP_200_OK)
async def delete_human(human_id: int, session: TSession) -> None:
    stmt = delete(Human).where(Human.id==human_id)
    await session.execute(stmt)
    await session.commit()


@humans_router.get('/{human_id}', response_model=HumanResponse)
async def get_human(human_id: int, session: TSession) -> HumanResponse:
    stmt = select(Human).filter_by(id=human_id)
    result = await session.execute(stmt)
    human = result.scalars().first()

    if human is None:
        raise HTTPException(
            status_code=404,
            detail=f'Human.id={human_id} is not already exists!'
        )

    return HumanResponse(
        id=human.id,
        title=human.title,
        phone_1=human.phone_1,
        phone_2=human.phone_2,
        is_firefigher=human.is_firefigher,
    )
