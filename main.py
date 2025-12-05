# -*- coding: utf-8 -*-

import sys

import uvicorn
from annotated_types import Annotated
from fastapi import FastAPI, HTTPException, Request, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.authentication import requires

from data_base.session import get_session, create_db_and_tables
from data_base.schema import User, CreateUserRequest, InfoResponse
from auth import authenticate_user


TSession = Annotated[AsyncSession, Depends(get_session)]


app = FastAPI()


@app.on_event('startup')
async def on_startup():
    await create_db_and_tables()


@app.get('/', name='home')
async def get_root(request: Request):
    return {'status': 200}


if __name__ == '__main__':
    try:
        uvicorn.run('main:app', reload=True)
    except KeyboardInterrupt:
        sys.exit()
