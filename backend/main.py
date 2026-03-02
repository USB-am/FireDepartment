# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from typing import Union, List, Dict, Callable
from contextlib import asynccontextmanager

import uvicorn
from annotated_types import Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base.session import get_session, create_db_and_tables
from data_base import schema as Schema
from data_base import models

# Routes
from routes import api_router


TSession = Annotated[AsyncSession, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    print(f'lifespan func is finished')


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

from auth import auth
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
