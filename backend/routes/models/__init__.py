from fastapi import APIRouter

from .users import users_router
from .fire_department import fd_router


model_router = APIRouter(prefix='/models')
model_router.include_router(users_router)
model_router.include_router(fd_router)
