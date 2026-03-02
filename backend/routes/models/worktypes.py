from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.schema import WorktypeResponse
from data_base.session import get_session
from data_base.models import Worktype


worktypes_router = APIRouter(prefix='/worktypes', tags=['Worktypes',])


TSession = Annotated[AsyncSession, Depends(get_session)]


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
