from pydantic_settings import BaseSettings
from pathlib import Path
from fastapi import HTTPException

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    APP_NAME: str = "SalesPrediction"
    APP_VERSION: str = "0.0.1"

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_DATABASE: str
    DB_HOST: str

    COOKIE_SECURE: bool
    COOKIE_SAMESITE: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    FRONTEND_URL: str

    class Config():
        env_file: str = ENV_PATH
        case_sensitive: bool = True

settings = Settings()