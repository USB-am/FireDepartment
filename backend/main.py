# -*- coding: utf-8 -*-

import sys
from typing import Dict, List
from datetime import datetime

import uvicorn
from annotated_types import Annotated
from fastapi import FastAPI, HTTPException, Request, Depends, Header, status
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.authentication import requires

from data_base.session import get_session, create_db_and_tables, Base
from data_base.schema import (
    CreateUserRequest,
    InfoResponse,
    LoginUserRequest,
    Emergency,
    CallResponse
)
from data_base import model as DBModel
from data_base.model import User, SecretKeyUser
from auth import authenticate_user, generate_secret_key


TSession = Annotated[AsyncSession, Depends(get_session)]


app = FastAPI()


@app.on_event('startup')
async def on_startup():
    await create_db_and_tables()


@app.get('/', name='home')
async def get_root(request: Request):
    x = request
    print(dir(x), x, type(x), sep='\n', end='\n'*3)
    return {'status': 200}


@app.post('/login', name='login', status_code=status.HTTP_200_OK)
async def post_login_user(request: LoginUserRequest, session: TSession):
    ''' Авторизация '''

    stmt = select(User).filter_by(email=request.email)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=400,
            detail=f'User with login "{request.email}" is not found!'
        )

    stmt = select(SecretKeyUser).filter_by(user_id=user.id)
    result = await session.execute(stmt)
    secret_key = result.scalars().first().secret_key

    user.last_used = datetime.now().isoformat()

    return {
        'status_code': 200,
        'detail': 'User is login',
        'secret_key': secret_key
    }


@app.post('/create-user', response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest, session: TSession) -> Dict:
    ''' Создание нового пользователя '''
    stmt = select(User).filter_by(username=request.username)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user:
        raise HTTPException(
            status_code=400,
            detail=f'User with username "{request.username}" already exists!'
        )

    secret_key = generate_secret_key(request.username)

    new_user = User(
        email=request.email,
        username=request.username,
        password=request.password,
        fd_number=request.fd_number,
        created_at=datetime.now().isoformat()
    )
    session.add(new_user)
    await session.commit()

    new_secret_key = SecretKeyUser(
        user_id=new_user.id,
        secret_key=secret_key
    )
    session.add(new_secret_key)
    await session.commit()

    return {
        'status_code': 201,
        'message': 'User created successfully',
        'user_id': new_user.id,
        'username': request.username,
        'secret_key': secret_key,
        'warning': 'Save this SECRET_KEY! It will not be shown again.'
    }


@app.get('/model', response_model=List[Emergency], status_code=status.HTTP_200_OK)
async def get_entries_by_model(request: Request,
                               model: str,
                               session: TSession,
                               q: str = '',
                               offset: int=0,
                               limit: int=100,
                               user: User = Depends(authenticate_user)
    ) -> List:
    ''' Получить записи из БД '''
    model = getattr(DBModel, model)
    stmt = (
        select(model)
        .where(func.lower(model.title).contains(func.lower(q)))
        .order_by(model.id)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    entries = result.scalars().all()
    return entries


@app.get('/call', response_model=CallResponse, status_code=status.HTTP_200_OK)
async def get_call_by_emergency_id(request: Request,
                                   id_: int,
                                   session: TSession,
                                   user: User = Depends(authenticate_user)
    ) -> CallResponse:
    ''' Получить данные о вызове по Emergency.id '''
    stmt = (
        select(DBModel.Emergency)
        .filter_by(id=id_)
        .options(selectinload(DBModel.Emergency.humans))
        .options(selectinload(DBModel.Emergency.shorts))
    )
    result = await session.execute(stmt)
    emergency = result.scalars().first()

    if emergency is None:
        raise HTTPException(
            status_code=404,
            detail=f'Emergency with id "{id_}" already exists!'
        )

    return CallResponse(
        title=emergency.title,
        description=emergency.description,
        humans=emergency.humans,
        shorts=emergency.shorts
    )


@app.get('/user-info', response_model=InfoResponse)
async def get_user_info(user: User = Depends(authenticate_user)):
    ''' Получение информации о пользователе (требуется SECRET_KEY) '''
    return InfoResponse(
        message=f'Hello, {user.username}!',
        user_id=user.id,
        username=user.username,
        timestamp=datetime.now().isoformat()
    )


@app.get('/protected-info', response_model=dict)
async def get_protected_info(user: User = Depends(authenticate_user)):
    ''' Получение защищенной информации (требуется SECRET_KEY) '''
    return {
        'message': 'This is protected information',
        'user_id': user.id,
        'username': user.username,
        'account_created': user.created_at,
        'last_activity': user.last_used or 'Never',
        'access_time': datetime.now().isoformat(),
        'status': 'authenticated'
    }


@app.get('/list-users', response_model=dict)
async def list_users(session: TSession, admin_key: str = Header(None, alias='ADMIN_KEY')):
    ''' Список всех пользователей (только для админа) '''
    ADMIN_SECRET = '123'

    if admin_key != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail='Admin access required')

    result = await session.execute(select(User))
    user_list = [{
            'username': user[0].username,
            'created_at': user[0].created_at,
            'last_used': user[0].last_used
        } for user in result.all()
    ]

    return {
        'total_users': len(user_list),
        'users': user_list
    }


@app.post('/rotate-key', response_model=dict)
async def rotate_secret_key(session: TSession, user: User = Depends(authenticate_user)):
    ''' Генерация нового SECRET_KEY для пользователя '''
    result = await session.scalars(select(SecretKeyUser)\
        .where(SecretKeyUser.user_id==user.id))
    secret_key = result.first()

    new_secret_key = generate_secret_key(user.username)
    user.secret_key = new_secret_key
    secret_key.secret_key = new_secret_key

    await session.commit()
    return {
        'message': 'SECRET_KEY rotated successfully',
        'user_id': user.id,
        'username': user.username,
        'new_secret_key': new_secret_key,
        'warning': 'Save this new SECRET_KEY! The old one is no longer valid.'
    }


@app.get('/list-entries', response_model=list)
async def get_all_entries(request: Request, session: TSession):
    ''' Список записей из таблицы (ВАЖНО! В headers должен быть
    передан аргумент model с названием таблицы для извлечения) '''

    model_name = request.headers.get('model')
    if model_name is None:
        raise HTTPException(status_code=400, detail='The \'model\' argument was not passed to headers')
    if not hasattr(DBModel, model_name):
        raise HTTPException(status_code=400, detail=f'There is no such thing as a \'{model_name}\' model')
    model = getattr(DBModel, model_name)
    limit = request.headers.get('limit', 20)
    offset = request.headers.get('offset', 0)
    result = await session.scalars(select(model)\
        .order_by().offset(offset).limit(limit))
    return result.all()


@app.middleware('http')
async def log_requests(request: Request, call_next):
    start_time = datetime.now()

    if request.url.path != '/':
        print(f'\n[{start_time}] {request.method} {request.url.path}')
        if 'SECRET_KEY' in request.headers:
            print(f'  Auth: Key present (hidden for security)')

    response = await call_next(request)

    process_time = (datetime.now() - start_time).total_seconds() * 1000
    print(f'  Completed in {process_time:.2f}ms - Status: {response.status_code}')
    return response


if __name__ == '__main__':
    try:
        uvicorn.run('main:app', reload=True)
    except KeyboardInterrupt:
        sys.exit()
