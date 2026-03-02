from fastapi import APIRouter

from .users import users_router
from .fire_department import fd_router
from .tags import tags_router
from .shorts import shorts_router
from .ranks import ranks_router
from .positions import positions_router
from .worktypes import worktypes_router
from .humans import humans_router
from .emergencies import emergencies_router
from .calls import calls_router


model_router = APIRouter(prefix='/models')

model_router.include_router(users_router)
model_router.include_router(fd_router)
model_router.include_router(tags_router)
model_router.include_router(shorts_router)
model_router.include_router(ranks_router)
model_router.include_router(positions_router)
model_router.include_router(worktypes_router)
model_router.include_router(humans_router)
model_router.include_router(emergencies_router)
model_router.include_router(calls_router)
