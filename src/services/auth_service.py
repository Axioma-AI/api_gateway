from typing import Any, Dict
from fastapi import HTTPException
from src.utils.http_client import HTTPClient
from src.config.settings import get_settings
import httpx

settings = get_settings()
http_client = HTTPClient(timeout=settings.timeout)

class AuthService:
    async def login(self, data: dict) -> dict:
        url = f"{settings.auth_service_url}/api/v1/auth/login"
        try:
            resp = await http_client.request("POST", url, json=data)
            return resp.json()
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            detail = exc.response.json()
            raise HTTPException(status_code=code, detail=detail)

    async def update(self, data: dict, token: str) -> dict:
        url = f"{settings.auth_service_url}/api/v1/user/profile"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            resp = await http_client.request("PUT", url, json=data, headers=headers)
            return resp.json()
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            detail = exc.response.json()
            raise HTTPException(status_code=code, detail=detail)

    async def get_profile(self, token: str) -> dict:
        url = f"{settings.auth_service_url}/api/v1/user/profile"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            resp = await http_client.request("GET", url, headers=headers)
            return resp.json()
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            detail = exc.response.json()
            raise HTTPException(status_code=code, detail=detail)
        
    async def create_subscription(self, token: str, data: Dict[str, Any]) -> Dict[str, Any]:
            url = f"{settings.suscription_service_url}/api/v1/subscriptions"
            params = {"token": token}  # token por query
            try:
                resp = await http_client.request("POST", url, json=data, params=params)
                return resp.json()
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json())

    async def verify_subscription(self, token: str) -> Dict[str, Any]:
        url = f"{settings.suscription_service_url}/api/v1/subscriptions/verify"
        params = {"token": token}  # token por query
        try:
            resp = await http_client.request("GET", url, params=params)
            return resp.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json())

    async def verify_subscription_post(self, token: str) -> Dict[str, Any]:
        url = f"{settings.suscription_service_url}/api/v1/subscriptions/verify"
        # El destino espera token en el **body**
        body = {"token": token}
        try:
            resp = await http_client.request("POST", url, json=body)
            return resp.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json())

    async def cancel_subscription(self, token: str) -> Dict[str, Any]:
        url = f"{settings.suscription_service_url}/api/v1/subscriptions/cancel"
        params = {"token": token}  # token por query
        try:
            resp = await http_client.request("POST", url, params=params)
            return resp.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json())

    async def verify_receipt(self, token: str, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{settings.suscription_service_url}/api/v1/subscriptions/verify-receipt"
        params = {"token": token}  # token por query
        try:
            resp = await http_client.request("POST", url, json=receipt_data, params=params)
            return resp.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json())