from fastapi import APIRouter

main_emergencies_router = APIRouter(prefix='/emergencies')


from .calls import calls_router
from .emergency import emergencies_router
from .firedepartment import firedepartments_router
from .humans import humans_router
from .positions import positions_router
from .ranks import ranks_router
from .shorts import shorts_router
from .tag import tags_router
from .worktypes import worktypes_router

main_emergencies_router.include_router(calls_router)
main_emergencies_router.include_router(emergencies_router)
main_emergencies_router.include_router(firedepartments_router)
main_emergencies_router.include_router(humans_router)
main_emergencies_router.include_router(positions_router)
main_emergencies_router.include_router(ranks_router)
main_emergencies_router.include_router(shorts_router)
main_emergencies_router.include_router(tags_router)
main_emergencies_router.include_router(worktypes_router)
