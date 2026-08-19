import uuid

from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserResponse(User, TokensResponse):
    model_config = ConfigDict(from_attributes=True)
