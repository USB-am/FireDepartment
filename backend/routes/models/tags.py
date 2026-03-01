from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.schema import TagResponse
from data_base.session import get_session
from data_base.models import Tag


tags_router = APIRouter(prefix='/tags', tags=['Tags',])


TSession = Annotated[AsyncSession, Depends(get_session)]


@tags_router.get('/{tag_id}', response_model=TagResponse)
async def get_tag(tag_id: int, session: TSession) -> TagResponse:
	stmt = select(Tag).filter_by(id=tag_id)
	result = await session.execute(stmt)
	tag = result.scalars().first()

	if tag is None:
		raise HTTPException(
			status_code=404,
			detail=f'Tag.id={tag_id} is not already exists!'
		)

	return TagResponse(
		id=tag.id,
		title=tag.title
	)
