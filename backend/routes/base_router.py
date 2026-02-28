from typing import Dict

from fastapi import APIRouter, Request


base_router_v1 = APIRouter(prefix='/api/v1')


@base_router_v1.get('/version')
async def get_version(request: Request) -> Dict:
    return {'api_version': '1.0.0'}
