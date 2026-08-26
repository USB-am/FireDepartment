from modules.utils.repository import BaseRepository
from modules.firedepartment.models import FireDepartment


class FireDepartmentRepository(BaseRepository[FireDepartment, int]):
    model = FireDepartment
