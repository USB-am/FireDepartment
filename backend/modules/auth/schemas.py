from typing import Optional, List, Dict, Any

from pydantic import BaseModel, EmailStr, ConfigDict


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class AccessTokenRequest(BaseModel):
    access_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
