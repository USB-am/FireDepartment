# -*- coding: utf-8 -*-

import sys
from typing import Dict
from datetime import datetime

import uvicorn
from annotated_types import Annotated
from fastapi import FastAPI, HTTPException, Request, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.authentication import requires

from data_base.session import get_session, create_db_and_tables
from data_base.schema import CreateUserRequest, InfoResponse
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


@app.post('/login', name='login')
async def post_login_user(request: Request):
    print(f'{request.cookies=}')
    print(f'{request.headers=}')
    return {'status': 200}


@app.post('/create-user', response_model=dict)
async def create_user(request: CreateUserRequest, session: TSession) -> Dict:
    ''' Создание нового пользователя '''
    x = request
    print(dir(x), x, type(x), sep='\n', end='\n'*3)
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
        username=request.username,
        secret_key=secret_key,
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
    # Простая проверка админского ключа (в реальном приложении используйте более безопасный подход)
    ADMIN_SECRET = '123'  # В реальном приложении храните в переменных окружения

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
    x = response.headers.keys()
    print(dir(x), x, type(x), sep='\n', end='\n'*5)
    return response


if __name__ == '__main__':
    try:
        uvicorn.run('main:app', reload=True)
    except KeyboardInterrupt:
        sys.exit()
