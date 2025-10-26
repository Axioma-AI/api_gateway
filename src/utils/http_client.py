from typing import Any, Dict, Optional, AsyncIterator, Tuple
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
    
    async def stream(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        json: Any = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[Tuple[Optional[int], Optional[str]]]:
        """
        Devuelve un iterador asíncrono que primero emite (status_code, None)
        y luego (None, line) por cada línea del cuerpo (SSE u otro).
        No levanta para 4xx/5xx; deja que el caller decida qué hacer.
        """
        client = await self._get_client()
        try:
            async with client.stream(
                method, url, headers=headers, json=json, params=params, timeout=timeout
            ) as resp:
                yield resp.status_code, None

                async for line in resp.aiter_lines():
                    if line is None:
                        continue
                    yield None, line
        except httpx.RequestError as exc:
            logger.error(f"Stream error while requesting {url}: {exc}")
            raise
