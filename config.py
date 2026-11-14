from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ORIGIN: list[str] = ["http://localhost:5173"]
    ACCESS_TOKEN_SECRET: SecretStr
    REFRESH_TOKEN_SECRET: SecretStr
    SQLALCHEMY_DATABASE_URL: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1  # 15 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days


settings = Settings()  # Loaded from .env file
