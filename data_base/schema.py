from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    secret_key: str
    created_at: str
    last_used: Optional[str] = None


# Модель для запроса создания пользователя
class CreateUserRequest(BaseModel):
    username: str


# Модель для ответа с информацией
class InfoResponse(BaseModel):
    message: str
    user_id: int
    username: str
    timestamp: str