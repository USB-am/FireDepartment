from fastapi import APIRouter

from routes.base_route import main_router_v1 as base_router


model_router = APIRouter(prefix='/model')
base_router.include_router(model_router)
