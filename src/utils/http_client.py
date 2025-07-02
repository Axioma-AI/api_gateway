from typing import Any, Dict, Optional
import httpx
from .logger import setup_logger

logger = setup_logger(__name__)

class HTTPClient:
    """Reusable asynchronous HTTP client."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if not self._client:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        json: Any = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        client = await self._get_client()
        try:
            response = await client.request(
                method, url, headers=headers, json=json, params=params
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTP error {exc.response.status_code} while requesting {url}: {exc.response.text}")
            raise
        except httpx.RequestError as exc:
            logger.error(f"Request error while requesting {url}: {exc}")
            raise
