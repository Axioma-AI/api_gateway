from src.utils.http_client import HTTPClient
from src.config.settings import get_settings
import httpx

settings = get_settings()
http_client = HTTPClient(timeout=settings.timeout)

class AxiomaService:
    async def get_articles(self, *, page: int = 1, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/getArticles"
        params = {"page": page}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        resp = await http_client.request("GET", url, params=params)
        return resp.json()

    async def search_articles(self, token: str, query: str, *, page: int = 1, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/search_text"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"query": query, "page": page}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        resp = await http_client.request("GET", url, headers=headers, params=params)
        return resp.json()

    async def get_article_pages(self, token: str, *, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/getArticlePages"
        headers = {"Authorization": f"Bearer {token}"}
        params: dict[str,str] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        resp = await http_client.request("GET", url, headers=headers, params=params)
        return resp.json()

    async def get_article_by_id(self, token: str, article_id: int) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/{article_id}"
        headers = {"Authorization": f"Bearer {token}"}
        resp = await http_client.request("GET", url, headers=headers)
        return resp.json()

    async def get_ai_articles_by_ids(self, token: str, ids: list[int]) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/aiArticlesQuery"
        headers = {"Authorization": f"Bearer {token}"}
        resp = await http_client.request("GET", url, headers=headers, params={"ids": ids})
        return resp.json()

    async def get_sources(self, token: str) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/get_all"
        headers = {"Authorization": f"Bearer {token}"}
        resp = await http_client.request("GET", url, headers=headers)
        return resp.json()

    async def search_sources(self, token: str, *, name: str | None = None, country: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/search"
        headers = {"Authorization": f"Bearer {token}"}
        params: dict[str,str] = {}
        if name:
            params["name"] = name
        if country:
            params["country"] = country
        resp = await http_client.request("GET", url, headers=headers, params=params)
        return resp.json()

    async def get_countries(self, token: str) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/countries"
        headers = {"Authorization": f"Bearer {token}"}
        resp = await http_client.request("GET", url, headers=headers)
        return resp.json()

    async def search_country(self, token: str, name: str) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/countries/search"
        headers = {"Authorization": f"Bearer {token}"}
        resp = await http_client.request("GET", url, headers=headers, params={"name": name})
        return resp.json()