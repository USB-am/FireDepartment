from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import model_router
from data_base.schema import UserResponse
from data_base.session import get_session
from data_base.models import User


TSession = Annotated[AsyncSession, Depends(get_session)]


@model_router.get('/user/{user_id}', response_model=UserResponse)
def get_user(user_id: int, session: TSession) -> UserResponse:
	stmt = select(User).filter_by(id=user_id)
	result = await session.execute(stmt)
	user = result.scalars().first()

	return UserResponse(
		id=user.id,
		email=user.email,
		username=user.username
	)
