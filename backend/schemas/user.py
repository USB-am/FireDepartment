import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, EmailStr,ConfigDict


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class User(BaseModel):
    id: int
    email: EmailStr
    username: str


class UserResponse(Tokens):
    id: int
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class FireDepartmentResponse(BaseModel):
    id: int
    title: str
    address: str


class CreateFireDepartmentRequest(BaseModel):
    title: str
    address: str
    users_ids: Optional[List[int]]


class UpdateFireDepartmentRequest(BaseModel):
    firedepartment_id: int
    fields: Dict[str, Any]


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    fd_number: int


class LoginUser(BaseModel):
    email: EmailStr
    password: str
