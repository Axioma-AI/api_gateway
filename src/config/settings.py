import logging
from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.utils.logger import setup_logger

logger = setup_logger(__name__, level=logging.DEBUG)

class Settings(BaseSettings):
    auth_service_url: str = "http://localhost:4000"
    axioma_service_url: str = "http://localhost:8001"
    timeout: int = 10
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env")

@cache
def get_settings() -> Settings:
    return Settings()
