import uuid

from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class UserResponse(User, Tokens):
    model_config = ConfigDict(from_attributes=True)
