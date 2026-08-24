from fastapi import APIRouter

from modules.auth.router import auth_router
from modules.users.router import users_router
from modules.firedepartment.router import fd_router


api_router = APIRouter(prefix='/api/v1')

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(fd_router)
