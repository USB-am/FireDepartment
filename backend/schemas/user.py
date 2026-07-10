import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    fd_number: Optional[str]
    password_hash: str
    created_at: str
    last_used: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str


class UserAuthResponse(UserResponse):
    token: str


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
