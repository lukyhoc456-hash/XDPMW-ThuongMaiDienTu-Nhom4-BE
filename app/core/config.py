import json
import os
from dotenv import load_dotenv
from typing import List

try:
    from pydantic_settings import BaseSettings
    from pydantic import validator
except ModuleNotFoundError:
    from pydantic import BaseSettings, validator

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


def parse_cors_origins(value):
    if value is None:
        return ['*']
    if isinstance(value, str):
        value = value.strip()
        if value in ('', '*'):
            return ['*']
        if value.startswith('[') and value.endswith(']'):
            try:
                parsed = json.loads(value)
                return [str(item) for item in parsed]
            except Exception:
                pass
        return [item.strip() for item in value.split(',') if item.strip()]
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return [str(value)]


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'FASTAPI BASE')
    SECRET_KEY: str = os.getenv('SECRET_KEY', '')
    API_PREFIX: str = ''
    BACKEND_CORS_ORIGINS: List[str] = ['*']
    DATABASE_URL: str = os.getenv('SQL_DATABASE_URL', '')
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM: str = 'HS256'
    LOGGING_CONFIG_FILE: str = os.path.join(BASE_DIR, 'logging.ini')

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def _parse_backend_cors_origins(cls, v):
        return parse_cors_origins(v)


settings = Settings()
