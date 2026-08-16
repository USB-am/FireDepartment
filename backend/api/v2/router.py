from fastapi import APIRouter

from .endpoints.users import users_router


api_router = APIRouter(prefix='/api/v2')

api_router.include_router(users_router)

