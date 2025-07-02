from fastapi import HTTPException, status
from src.utils.http_client import HTTPClient
from src.config.settings import get_settings
from src.utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)
http_client = HTTPClient(timeout=settings.timeout)


class AuthService:
    async def login(self, data: dict) -> dict:
        url = f"{settings.auth_service_url}/auth/login"
        response = await http_client.request("POST", url, json=data)
        return response.json()

    async def update(self, data: dict, token: str) -> dict:
        url = f"{settings.auth_service_url}/user/profile"
        headers = {"Authorization": f"Bearer {token}"}
        response = await http_client.request("PUT", url, json=data, headers=headers)
        return response.json()

    async def get_profile(self, token: str) -> dict:
        url = f"{settings.auth_service_url}/user/profile"
        headers = {"Authorization": f"Bearer {token}"}
        response = await http_client.request("GET", url, headers=headers)
        return response.json()
