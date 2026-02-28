from fastapi import APIRouter

from .models import model_router as models_router


api_router = APIRouter(prefix='/api/v1')
api_router.include_router(models_router)
