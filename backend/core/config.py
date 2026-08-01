from pydantic_settings import BaseSettings, SettingsConfigDict
from authx import AuthX, AuthXConfig


class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite+aiosqlite:///./data/firedepartment.db'
    JWT_SECRET_KEY: str = 'my_secret_key'
    JWT_TOKEN_LOCATION: list[str] = ['headers']

    # Set True for production
    SECURE: bool = False
    HTTP_ONLY: bool = True

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()

config = AuthXConfig(
    JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
    JWT_TOKEN_LOCATION=settings.JWT_TOKEN_LOCATION
)
auth = AuthX(config=config)
