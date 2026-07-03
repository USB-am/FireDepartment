from typing import Dict
from datetime import datetime

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from data_base.schema import ErrorResponse


base_router_v1 = APIRouter(prefix='/api/v1')


@base_router_v1.get('/version')
async def get_version(request: Request) -> Dict:
    return {'api_version': '1.0.0'}


@base_router_v1.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error='INTERNAL_SERVER_ERROR',
            message='An unexpected error occurred.',
            path=request.url.path,
            timestamp=datetime.now()
        ).model_dump()
    )
