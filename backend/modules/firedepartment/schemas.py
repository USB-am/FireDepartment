from pydantic import BaseModel, ConfigDict


class FireDepartmentResponse(BaseModel):
    id: int
    title: str
    address: str

    model_config = ConfigDict(from_attributes=True)


class CreateFireDepartmentRequest(BaseModel):
    title: str
    address: str


class UpdateFireDepartmentRequest(BaseModel):
    id: int
    title: str
    address: str
