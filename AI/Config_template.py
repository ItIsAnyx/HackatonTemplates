from pydantic_settings import BaseSettings
from fastapi import HTTPException

class Settings(BaseSettings):
    APP_NAME: str = "Example"
    BACKEND_KEY: str
    MODEL_NAME: str
    DEEPSEEK_API_KEY: str

    MAX_REQUEST_LENGTH: str

    MAX_FILE_SIZE_MB: int = 10

    class Config():
        env_file = ".env"
        case_sensitive = True

settings = Settings()

def validate_key(backend_key: str):
    if backend_key != settings.BACKEND_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: BACKEND_KEY is invalid")