from authx import AuthX, AuthXConfig


DATABASE_URL = 'sqlite+aiosqlite:///./firedepartment.db'

config = AuthXConfig(
    JWT_SECRET_KEY='my_secret_key',
    JWT_TOKEN_LOCATION=['headers']
)
auth = AuthX(config=config)

SECURE = False  # Set True for production
