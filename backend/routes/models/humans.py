from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.schema import HumanResponse
from data_base.session import get_session
from data_base.models import Human


humans_router = APIRouter(prefix='/humans', tags=['Humans',])


TSession = Annotated[AsyncSession, Depends(get_session)]


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
