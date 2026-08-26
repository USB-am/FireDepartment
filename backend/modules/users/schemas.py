import uuid

from pydantic import BaseModel, EmailStr, ConfigDict


class ShortUserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserResponse(ShortUserResponse, TokensResponse):
    model_config = ConfigDict(from_attributes=True)


class UserProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    call_sign: str

    model_config = ConfigDict(from_attributes=True)
