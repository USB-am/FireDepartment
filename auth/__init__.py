import hashlib
import secrets
from datetime import datetime

from fastapi import HTTPException, Header

from data_base.model import User


def generate_secret_key(username: str) -> str:
    """Генерация уникального секретного ключа"""
    timestamp = datetime.now().isoformat()
    random_part = secrets.token_hex(16)
    data = f"{username}{timestamp}{random_part}"
    
    # Используем хеш для создания ключа
    return hashlib.sha256(data.encode()).hexdigest()


async def authenticate_user(secret_key: str = Header(..., alias="SECRET_KEY")) -> User:
    """
    Функция для аутентификации пользователя по SECRET_KEY
    """
    if secret_key not in secret_keys_db:
        raise HTTPException(
            status_code=401,
            detail="Invalid SECRET_KEY",
            headers={"WWW-Authenticate": "SecretKey"}
        )
    
    user_id = secret_keys_db[secret_key]
    user = users_db.get(user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Обновляем время последнего использования
    user.last_used = datetime.now().isoformat()
    users_db[user_id] = user
    save_data()
    
    return user
