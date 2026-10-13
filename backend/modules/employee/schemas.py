import uuid

from pydantic import BaseModel, ConfigDict


class EmployeeResponse(BaseModel):
    id: uuid.UUID
    surname: str
    name: str
    patronymic: str

    model_config = ConfigDict(from_attributes=True)
