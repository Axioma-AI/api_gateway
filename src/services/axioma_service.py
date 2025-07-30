from src.schema.article_models import NewsFavoritesCoreRequest
from src.utils.http_client import HTTPClient
from src.config.settings import get_settings

settings = get_settings()
http_client = HTTPClient(timeout=settings.timeout)

class AxiomaService:
    async def get_articles(self, *, page: int = 1, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/getArticles"
        params = {"page": page}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        resp = await http_client.request("GET", url, params=params)
        return resp.json()

    async def search_articles_by_text(self, query: str, *, page: int = 1, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/search_text"
        params = {"query": query, "page": page}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        resp = await http_client.request("GET", url, params=params)
        return resp.json()

    async def get_article_pages(self, *, start_date: str | None = None, end_date: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/getArticlePages"
        params: dict[str, str] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        resp = await http_client.request("GET", url, params=params)
        return resp.json()

    async def get_article_by_id(self, article_id: int) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/{article_id}"
        resp = await http_client.request("GET", url)
        return resp.json()

    async def get_ai_articles_by_ids(self, ids: list[int]) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/aiArticlesQuery"
        resp = await http_client.request("GET", url, params={"ids": ids})
        return resp.json()

    # Métodos para sources
    async def get_sources(self) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/sources/"
        resp = await http_client.request("GET", url)
        return resp.json()

    async def search_sources(self, *, name: str | None = None, country: str | None = None) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/sources/search"
        params: dict[str, str] = {}
        if name:
            params["name"] = name
        if country:
            params["country"] = country
        resp = await http_client.request("GET", url, params=params)
        return resp.json()

    async def get_countries(self) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/sources/countries"
        resp = await http_client.request("GET", url)
        return resp.json()

    async def search_country(self, name: str) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/sources/countries/search"
        resp = await http_client.request("GET", url, params={"name": name})
        return resp.json()
    
    async def get_favorites(self, page: int, token) -> dict:
        url = f"{settings.axioma_service_url}/api/v1/articles/favorites"
        headers = {"Authorization": f"Bearer {token}"}
        resp = await http_client.request("GET", url, params={"page": page}, headers=headers)
        return resp.json()
    
    async def add_favorite(self, newFavorite: NewsFavoritesCoreRequest, token: str) -> dict:
        url = f"{settings.auth_service_url}/favorite-news"
        headers = {"Authorization": f"Bearer {token}"}
        resp = await http_client.request("POST", url, json=newFavorite.model_dump(), headers=headers)
        return resp.json()
    
    async def delete_favorite(self, newFavorite: NewsFavoritesCoreRequest, token: str) -> dict:
        url = f"{settings.auth_service_url}/favorite-news"
        headers = {"Authorization": f"Bearer {token}"}
        resp = await http_client.request("DELETE", url, json=newFavorite.model_dump(),  headers=headers)
        return resp.json()
    
    async def get_interests(self, token: str) -> dict:
        """
        Obtiene todos los interests del usuario autenticado.
        """
        http_client = HTTPClient(timeout=30.0)
        url = f"{settings.axioma_service_url}/api/v1/interests"
        headers = {"Authorization": f"Bearer {token}"}
        resp = await http_client.request("GET", url, headers=headers)
        return resp.json()
    
    async def add_interest(self, keyword: str, token: str) -> dict:
        """
        Añade un nuevo interest al usuario autenticado.
        """
        url = f"{settings.auth_service_url}/interests-user"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"keyword": keyword}
        resp = await http_client.request("POST", url, params=params, headers=headers)
        return resp.json()
    
    async def get_recommended_articles(self) -> dict:
        """
        Obtiene 5 artículos recomendados aleatorios de hoy o ayer si no hay artículos de hoy.
        Retorna 5 artículos aleatorios que se refrescan en cada petición.
        """
        url = f"{settings.axioma_service_url}/api/v1/articles/recommended"
        resp = await http_client.request("GET", url)
        return resp.json()
    
    async def get_source_by_id(self, source_id: int) -> dict:
        """
        Obtiene una fuente específica por su ID.
        """
        url = f"{settings.axioma_service_url}/api/v1/sources/{source_id}"
        resp = await http_client.request("GET", url)
        return resp.json()
    
    async def get_country_by_id(self, country_id: int) -> dict:
        """
        Obtiene un país específico por su ID.
        """
        url = f"{settings.axioma_service_url}/api/v1/sources/countries/{country_id}"
        resp = await http_client.request("GET", url)
        return resp.json()