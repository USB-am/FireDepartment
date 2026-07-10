from fastapi import APIRouter

from .endpoints.emergencies import main_emergencies_router
from .endpoints.users import users_router


api_router = APIRouter(prefix='/api/v1')

api_router.include_router(main_emergencies_router)
api_router.include_router(users_router)
