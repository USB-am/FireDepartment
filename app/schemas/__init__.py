from pydantic import BaseModel, EmailStr


class AuthFormModel(BaseModel):
    email: EmailStr
    password: str


class RegisterFormModel(BaseModel):
    email: EmailStr
    username: str
    password: str
