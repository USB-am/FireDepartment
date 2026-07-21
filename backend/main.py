# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from typing import Callable
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import api_router
from core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    print(f'lifespan func is finished')


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

origins = [
    '*',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['Set-Cookie'],
)

from core.config import auth
auth.handle_errors(app)


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
