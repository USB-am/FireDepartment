# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from typing import Any, Dict, Callable
from contextlib import asynccontextmanager

import uvicorn
from annotated_types import Annotated
from authx import AuthX, AuthXConfig
from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.schema import LoginUserRequest
from data_base.session import get_session, create_db_and_tables


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
    # Authorization
)

auth = AuthX(config=config)
auth.handle_errors(app)


@app.post('/login')
async def login(login_form: LoginUserRequest, session: TSession):
    if login_form.email == '123' and login_form.password == '123':
        token = auth.create_access_token(uid=login_form.email)
        return {'access_token': token}
    raise HTTPException(
        status_code=401,
        detail='Invalid email or password!'
    )


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
