from src.utils.http_client import HTTPClient
from src.config.settings import get_settings

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

    async def search_articles_by_text(self, query: str, *, page: int = 1, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/search_text"
        params = {"query": query, "page": page}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        resp = await http_client.request("GET", url, params=params)
        return resp.json()

    async def get_article_pages(self, *, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/getArticlePages"
        params: dict[str, str] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        resp = await http_client.request("GET", url, params=params)
        return resp.json()

    async def get_article_by_id(self, article_id: int) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/{article_id}"
        resp = await http_client.request("GET", url)
        return resp.json()

    async def get_ai_articles_by_ids(self, ids: list[int]) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/aiArticlesQuery"
        resp = await http_client.request("GET", url, params={"ids": ids})
        return resp.json()

    # Métodos para sources (si los necesitas)
    async def get_sources(self) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/get_all"
        resp = await http_client.request("GET", url)
        return resp.json()

    async def search_sources(self, *, name: str | None = None, country: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/search"
        params: dict[str, str] = {}
        if name:
            params["name"] = name
        if country:
            params["country"] = country
        resp = await http_client.request("GET", url, params=params)
        return resp.json()

    async def get_countries(self) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/countries"
        resp = await http_client.request("GET", url)
        return resp.json()

    async def search_country(self, name: str) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/countries/search"
        resp = await http_client.request("GET", url, params={"name": name})
        return resp.json()