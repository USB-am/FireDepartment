from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import update, delete

from auth import TSession
from data_base.schema import WorktypeResponse, CreateWorktypeRequest, UpdateWorktypeRequest
from data_base.models import Worktype, Human


worktypes_router = APIRouter(prefix='/worktypes', tags=['Worktypes',])


@worktypes_router.post('/create', response_model=WorktypeResponse, status_code=status.HTTP_201_CREATED)
async def create_worktype(form: CreateWorktypeRequest, session: TSession) -> WorktypeResponse:
    title = form.title
    stmt = select(Worktype).filter_by(title=title)
    result = await session.execute(stmt)
    worktype = result.scalars().first()

    if worktype is not None:
        raise HTTPException(
            status_code=409,
            detail=f'Worktype.title=`{title}` is already exists.'
        )

    humans_ids = form.humans_ids
    stmt = select(Human).where(Human.id.in_(humans_ids))
    result = await session.execute(stmt)
    humans = result.scalars().all()

    new_worktype = Worktype(
        title=title,
        start_work_day=form.start_work_day,
        finish_work_day=form.finish_work_day,
        work_day_range=form.work_day_range,
        week_day_range=form.week_day_range,
        humans=humans
    )
    session.add(new_worktype)
    await session.commit()

    return WorktypeResponse(
        id=new_worktype.id,
        title=new_worktype.title,
        start_work_day=new_worktype.start_work_day,
        finish_work_day=new_worktype.finish_work_day,
        work_day_range=new_worktype.work_day_range,
        week_day_range=new_worktype.week_day_range,
    )


@worktypes_router.put('/update/{worktype_id}', status_code=status.HTTP_201_CREATED)
async def update_worktype(form: UpdateWorktypeRequest, session: TSession) -> None:
    worktype_id = form.worktype_id
    fields = form.fields

    stmt = update(Worktype).where(Worktype.id==worktype_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


@worktypes_router.delete('/delete/{worktype_id}', status_code=status.HTTP_200_OK)
async def delete_worktype(worktype_id: int, session: TSession) -> None:
    stmt = delete(Worktype).where(Worktype.id==worktype_id)
    await session.execute(stmt)
    await session.commit()


@worktypes_router.get('/{worktype_id}', response_model=WorktypeResponse)
async def get_worktype(worktype_id: int, session: TSession) -> WorktypeResponse:
    stmt = select(Worktype).filter_by(id=worktype_id)
    result = await session.execute(stmt)
    worktype = result.scalars().first()

    if worktype is None:
        raise HTTPException(
            status_code=404,
            detail=f'Worktype.id={worktype_id} is not already exists!'
        )

    return WorktypeResponse(
        id=worktype.id,
        title=worktype.title,
        start_work_day=worktype.start_work_day,
        finish_work_day=worktype.finish_work_day,
        work_day_range=worktype.work_day_range,
        week_day_range=worktype.week_day_range,
    )
