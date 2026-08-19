# -*- coding: utf-8 -*-

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send

from core.database import create_db_and_tables
from modules.router import api_router


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


class LogRequestsMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        start_time = time.perf_counter()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                process_time = (time.perf_counter() - start_time) * 1000
                print(f'Completed in {process_time:.2f}ms - Status: {status_code}')
            await send(message)
        await self.app(scope, receive, send_wrapper)


app.add_middleware(LogRequestsMiddleware)
