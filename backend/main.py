# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from typing import Union, List, Dict, Callable
from contextlib import asynccontextmanager

import uvicorn
from annotated_types import Annotated
from authx import AuthX, AuthXConfig
from fastapi import FastAPI, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.session import get_session, create_db_and_tables
from data_base import schema as Schema
from data_base import models


TSession = Annotated[AsyncSession, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    print(f'lifespan func is finished')


app = FastAPI(lifespan=lifespan)
config = AuthXConfig(
    JWT_SECRET_KEY='my_secret_key',
    JWT_TOKEN_LOCATION=['headers']
)

auth = AuthX(config=config)
auth.handle_errors(app)


@app.post('/login', status_code=status.HTTP_201_CREATED)
async def login(login_form: Schema.LoginUser, session: TSession):
    if login_form.email == 'test' and login_form.password == 'test':
        token = auth.create_access_token(uid=login_form.email)
        return {'access_token': token}
    raise HTTPException(
        status_code=401,
        detail='Invalid email or password!'
    )


@app.get('/model/{tablename}/{entry_id}',
         response_model=Union[
            Schema.Tag,
            Schema.Rank,
            Schema.Position,
            Schema.Emergency,
         ],
         dependencies=[Depends(auth.access_token_required)])
async def get_entry_by_id(tablename: str, entry_id: int, session: TSession):

    if (model:=getattr(models, tablename, None)) is None:
        raise HTTPException(
            status_code=404,
            detail=f'Tablename "{tablename}" not already exists!'
        )

    stmt = select(model).filter_by(id=entry_id)
    result = await session.execute(stmt)
    entry = result.scalars().first()

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=f'{tablename}.id={entry_id} is not already exists!'
        )

    return getattr(Schema, tablename).model_validate(entry)


@app.get('/protected', dependencies=[Depends(auth.access_token_required)])
def protected():
    return {'message': 'Hello, World!'}


@app.middleware('http')
async def log_requests(request: Request, call_next: Callable):
    start_time = datetime.now()

    response = await call_next(request)

    process_time = (datetime.now() - start_time).total_seconds() * 1000
    print(f'Completed in {process_time:.2f}ms - Status: {response.status_code}')
    return response


if __name__ == '__main__':
    try:
        uvicorn.run('main:app', reload=True)
    except KeyboardInterrupt:
        sys.exit()
