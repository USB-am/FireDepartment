from pydantic import BaseModel, ConfigDict


class FireDepartmentResponse(BaseModel):
    id: int
    title: str
    address: str

    model_config = ConfigDict(from_attributes=True)
