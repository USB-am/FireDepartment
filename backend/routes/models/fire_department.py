from fastapi import APIRouter, Depends, HTTPException
from annotated_types import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.session import get_session
from data_base.models import FireDepartment
from data_base.schema import FireDepartmentResponse


fd_router = APIRouter(prefix='/firedepartments', tags=['Fire departments',])


TSession = Annotated[AsyncSession, Depends(get_session)]


@fd_router.get('/{fd_id}', response_model=FireDepartmentResponse)
async def get_firedepartment(fd_id: int, session: TSession) -> FireDepartmentResponse:
	stmt = select(FireDepartment).filter_by(id=fd_id)
	result = await session.execute(stmt)
	firedepartment = result.scalars().first()

	if firedepartment is None:
		raise HTTPException(
			status_code=404,
			detail=f'FireDepartment.id={fd_id} is not already exists!'
		)

	return FireDepartmentResponse(
		id=firedepartment.id,
		title=firedepartment.title,
		address=firedepartment.address
	)
