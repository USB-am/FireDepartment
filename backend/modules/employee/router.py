from fastapi import APIRouter, HTTPException

from core.database import TSession
from core.dependencies import TCurrentUser, RequireRole
from core.security import Role
from modules.employee.schemas import EmployeeResponse
from modules.employee.models import Employee


employee_router = APIRouter(prefix='/employee', tags=['Employee',])


@employee_router.post('/create', response_model=EmployeeResponse)
async def create_employee(session: TSession):
    pass
