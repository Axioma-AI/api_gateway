from datetime import date
import json
from typing import Optional, AsyncIterator
import httpx
from fastapi import HTTPException

from src.schema.article_models import ChatRequest, NewsFavoritesCoreRequest
from src.utils.http_client import HTTPClient
from src.config.settings import get_settings

settings = get_settings()
http_client = HTTPClient(timeout=settings.timeout)

class AxiomaService:
    async def _request_json(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[dict] = None,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> dict:
        try:
            resp = await http_client.request(method, url, headers=headers, json=json, params=params)
            return resp.json()
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            try:
                detail = exc.response.json()
            except Exception:
                detail = exc.response.text
            raise HTTPException(status_code=code, detail=detail)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=str(exc))
    async def get_articles(self, *, page: int = 1, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/getArticles"
        params = {"page": page}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return await self._request_json("GET", url, params=params)

    async def search_articles_by_text(self, query: str, *, page: int = 1, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/search_text"
        params = {"query": query, "page": page}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return await self._request_json("GET", url, params=params)

    async def get_article_pages(self, *, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/getArticlePages"
        params: dict[str, str] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return await self._request_json("GET", url, params=params)

    async def get_article_by_id(self, article_id: int) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/{article_id}"
        return await self._request_json("GET", url)

    async def get_ai_articles_by_ids(self, ids: list[int]) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/aiArticlesQuery"
        return await self._request_json("GET", url, params={"ids": ids})

    # Métodos para sources
    async def get_sources(self) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/sources/"
        return await self._request_json("GET", url)

    async def search_sources(self, *, name: str | None = None, country: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/sources/search"
        params: dict[str, str] = {}
        if name:
            params["name"] = name
        if country:
            params["country"] = country
        return await self._request_json("GET", url, params=params)

    async def get_countries(self) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/sources/countries"
        return await self._request_json("GET", url)

    async def search_country(self, name: str) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/sources/countries/search"
        return await self._request_json("GET", url, params={"name": name})
    
    async def get_favorites(self, page: int, token) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/favorites"
        headers = {"Authorization": f"Bearer {token}"}
        return await self._request_json("GET", url, params={"page": page}, headers=headers)
    
    async def add_favorite(self, newFavorite: NewsFavoritesCoreRequest, token: str) -> dict:
        url = f"{settings.auth_service_url}/api/v1/favorite-news"
        headers = {"Authorization": f"Bearer {token}"}
        return await self._request_json("POST", url, json=newFavorite.model_dump(), headers=headers)
    
    async def delete_favorite(self, newFavorite: NewsFavoritesCoreRequest, token: str) -> dict:
        url = f"{settings.auth_service_url}/api/v1/favorite-news"
        headers = {"Authorization": f"Bearer {token}"}
        return await self._request_json("DELETE", url, json=newFavorite.model_dump(), headers=headers)
    
    async def get_interests(self, token: str) -> dict:
        """
        Obtiene todos los interests del usuario autenticado.
        """
        url = f"{settings.auth_service_url}/api/v1/interests-user"
        headers = {"Authorization": f"Bearer {token}"}
        return await self._request_json("GET", url, headers=headers)
    
    async def add_interest(self, keyword: str, token: str) -> dict:
        """
        Añade un nuevo interest al usuario autenticado.
        """
        url = f"{settings.auth_service_url}/api/v1/interests-user"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"keyword": keyword}
        return await self._request_json("POST", url, params=params, headers=headers)
    
    async def get_recommended_articles(self) -> dict:
        """
        Obtiene 5 artículos recomendados aleatorios de hoy o ayer si no hay artículos de hoy.
        Retorna 5 artículos aleatorios que se refrescan en cada petición.
        """
        url = f"{settings.axioma_service_url}/api/v1/articles/recommended"
        return await self._request_json("GET", url)
    
    async def get_source_by_id(self, source_id: int) -> dict:
        """
        Obtiene una fuente específica por su ID.
        """
        url = f"{settings.axioma_service_url}/api/v1/sources/{source_id}"
        return await self._request_json("GET", url)
    
    async def get_country_by_id(self, country_id: int) -> dict:
        """
        Obtiene un país específico por su ID.
        """
        url = f"{settings.axioma_service_url}/api/v1/sources/countries/{country_id}"
        return await self._request_json("GET", url)
    
    async def search_articles_by_source(
        self,
        source_id: int,
        query: Optional[str] = None,
        page: int = 1,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> dict:
        """
        Busca artículos por fuente de noticias.
        """
        url = f"{settings.axioma_service_url}/api/v1/articles/search_by_source"

        params = {
            "source_id": source_id,
            "query": query,
            "page": page,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        }

        params = {k: v for k, v in params.items() if v is not None}

        return await self._request_json("GET", url, params=params)

    async def get_interests_by_interest(
        self,
        interest: str,
        page: int = 1,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict:
        """
        Search articles by interest term with pagination and date filters.
        """
        url = f"{settings.axioma_service_url}/api/v1/by-interest"
        params = {
            "interest": interest,
            "page": page,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return await self._request_json("GET", url, params=params)

    async def get_analysis(
        self,
        query: str,
        interval: int,
        unit: str
    ) -> dict:
        """
        Realiza un análisis de sentimientos de noticias basado en una consulta de texto y un rango de tiempo específico.
        """
        url = f"{settings.axioma_service_url}/api/v1/analysis"
        params = {
            "query": query,
            "interval": interval,
            "unit": unit
        }
        return await self._request_json("GET", url, params=params)
    
    async def get_sentiment_counts_data_analysis(
        self,
        scope: str,
        value: Optional[str] = None,
        query: Optional[str] = None,
    ) -> dict:
        """
        Llama al endpoint /api/v1/data-analysis/sentiments del servicio Axioma.

        - scope: 'day' | 'month' | 'year'
        - value (opcional):
            * day   → 'dd/mm/yyyy'
            * month → 'mm/yyyy'
            * year  → 'yyyy'
          Si es None, el backend usa la fecha actual.
        """
        url = f"{settings.axioma_service_url}/api/v1/data-analysis/sentiments"
        params: dict[str, str] = {"scope": scope}
        if value is not None:
            params["value"] = value
        if query is not None:
            params["query"] = query

        return await self._request_json("GET", url, params=params)
    
    async def update_interests(self, interests: list[str], token: str) -> dict:
        """
        Actualiza los intereses del usuario autenticado.
        """
        url = f"{settings.auth_service_url}/api/v1/interests-user"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"interests": interests}
        return await self._request_json("PUT", url, json=payload, headers=headers)
    
    async def consult_article_stream(
        self,
        article_id: int,
        chat_request: ChatRequest,
        token: str,
    ) -> AsyncIterator[bytes]:
        """
        Proxy streaming SSE hacia el servicio de artículos usando HTTPClient.stream.
        Devuelve bytes listos para StreamingResponse (líneas terminadas en '\n').
        """
        url = f"{settings.axioma_service_url}/api/v1/articles/{article_id}/consult"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "text/event-stream",
            "Cache-Control": "no-cache",
        }

        try:
            first = True
            async for status, line in http_client.stream(
                "POST", url, headers=headers, json=chat_request.model_dump(), timeout=None
            ):
                if first:
                    first = False
                    if status is not None and status != 200:
                        err = {"error": "Upstream error", "status": status}
                        yield f"data: {json.dumps(err)}\n\n".encode("utf-8")
                        return
                    continue

                if line is None:
                    continue
                yield (line + "\n").encode("utf-8")

        except Exception as e:
            err = {"error": f"Gateway SSE proxy error: {str(e)}"}
            yield f"data: {json.dumps(err)}\n\n".encode("utf-8")
        
    async def consult_multiple_articles_stream(
        self,
        chat_request,  # MultipleArticlesChatRequest
    ) -> AsyncIterator[bytes]:
        """
        Proxy streaming SSE hacia el servicio Axioma para consulta multi-artículo.
        Devuelve bytes listos para StreamingResponse (líneas terminadas en '\n').
        """
        url = f"{settings.axioma_service_url}/api/v1/articles/consult"
        headers = {
            "Accept": "text/event-stream",
            "Cache-Control": "no-cache",
        }

        try:
            first = True
            async for status, line in http_client.stream(
                "POST",
                url,
                headers=headers,
                json=chat_request.model_dump(),
                timeout=None,  # importante para SSE
            ):
                if first:
                    first = False
                    if status is not None and status != 200:
                        err = {"error": "Upstream error", "status": status}
                        yield f"data: {json.dumps(err)}\n\n".encode("utf-8")
                        return
                    continue

                if line is None:
                    continue

                # line ya viene tipo: "data: {...}" o "data: [DONE]"
                yield (line + "\n").encode("utf-8")

        except Exception as e:
            err = {"error": f"Gateway SSE proxy error: {str(e)}"}
            yield f"data: {json.dumps(err)}\n\n".encode("utf-8")

    async def search_article_ids(
        self,
        query: str,
        *,
        page: int = 1,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict:
        """
        Proxy al endpoint:
        GET /api/v1/articles/search/ids
        Devuelve IDs y paginación.
        """
        url = f"{settings.axioma_service_url}/api/v1/articles/search/ids"
        params: dict[str, object] = {
            "query": query,
            "page": page,
        }
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date

        return await self._request_json("GET", url, params=params)

    async def get_last_30_days_sentiments(
        self,
        query: str,
    ) -> dict:
        """
        Proxy al endpoint:
        GET /api/v1/data-analysis/sentiments/last-30-days
        """
        url = f"{settings.axioma_service_url}/api/v1/data-analysis/sentiments/last-30-days"
        params = {"query": query}
        return await self._request_json("GET", url, params=params)

