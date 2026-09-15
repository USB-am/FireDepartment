import uuid

from pydantic import BaseModel, ConfigDict


class UserProfileResponse(BaseModel):
    id: uuid.UUID
    call_sign: str
    firedepartment_id: int | None

    model_config = ConfigDict(from_attributes=True)
