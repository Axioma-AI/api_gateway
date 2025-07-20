from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from datetime import date
from src.dependencies.auth import require_token
from src.services.axioma_service import AxiomaService
from src.schema.article_models import (
    ArticleResponseModel, 
    ArticlePageCountResponseModel, 
    ArticleAIResponseModel,
    AIRequestIDs,
    NewsFavoritesCoreRequest,
    UpdateFavoritesResponse
)

router = APIRouter(
    prefix="/gateway/articles",
    tags=["Articles"],
    dependencies=[Depends(require_token)]
)

service = AxiomaService()

@router.get("/favorite")
async def get_favorites(
    page: int = Query(1, ge=1, description="Número de página para paginación"),
    token: str = Depends(require_token)
):
    """
    Versión POST para obtener artículos de IA (para listas grandes de IDs).
    """
    return await service.get_favorites(page, token)

@router.post("/favorite", response_model = UpdateFavoritesResponse)
async def add_favorite(
    newFavorite: NewsFavoritesCoreRequest,
    token: str = Depends(require_token)
):
    """
    Versión POST para obtener artículos de IA (para listas grandes de IDs).
    """
    return await service.add_favorite(newFavorite, token)

@router.delete("/favorite", response_model = UpdateFavoritesResponse)
async def delete_favorite(
    newFavorite: NewsFavoritesCoreRequest, 
    token: str = Depends(require_token)
):
    """
    Versión POST para obtener artículos de IA (para listas grandes de IDs).
    """
    return await service.delete_favorite(newFavorite, token)

@router.get("/getArticles", response_model=List[ArticleResponseModel])
async def get_articles(
    page: int = Query(default=1, ge=1, description="Número de página (50 resultados por página)"),
    start_date: Optional[date] = Query(
        default=None,
        description="Fecha de inicio en formato YYYY-MM-DD (por defecto: hoy)"
    ),
    end_date: Optional[date] = Query(
        default=None,
        description="Fecha de fin en formato YYYY-MM-DD (por defecto: hoy)"
    )
):
    """
    Obtiene artículos con paginación y filtros de fecha.
    Equivalente a GET /getArticles del servicio original.
    """
    # Convertir dates a strings si es necesario
    start_date_str = start_date.isoformat() if start_date else None
    end_date_str = end_date.isoformat() if end_date else None
    
    return await service.get_articles(
        page=page, 
        start_date=start_date_str, 
        end_date=end_date_str
    )

@router.get("/search_text", response_model=List[ArticleResponseModel])
async def search_articles_by_text(
    query: str = Query(..., description="Texto a buscar en título o contenido (modo booleano)"),
    page: int = Query(default=1, ge=1, description="Número de página (50 resultados por página)"),
    start_date: Optional[date] = Query(default=None, description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(default=None, description="Fecha de fin (YYYY-MM-DD)")
):
    """
    Busca artículos por texto en título o contenido.
    Equivalente a GET /search_text del servicio original.
    """
    # Convertir dates a strings si es necesario
    start_date_str = start_date.isoformat() if start_date else None
    end_date_str = end_date.isoformat() if end_date else None
    
    return await service.search_articles_by_text(
        query=query,
        page=page,
        start_date=start_date_str,
        end_date=end_date_str
    )

@router.get("/getArticlePages", response_model=ArticlePageCountResponseModel)
async def get_article_pages(
    start_date: Optional[date] = Query(default=None, description="Formato: YYYY-MM-DD"),
    end_date: Optional[date] = Query(default=None, description="Formato: YYYY-MM-DD")
):
    """
    Obtiene el número total de páginas disponibles.
    Equivalente a GET /getArticlePages del servicio original.
    """
    # Convertir dates a strings si es necesario
    start_date_str = start_date.isoformat() if start_date else None
    end_date_str = end_date.isoformat() if end_date else None
    
    return await service.get_article_pages(
        start_date=start_date_str,
        end_date=end_date_str
    )

@router.get("/aiArticlesQuery", response_model=List[ArticleAIResponseModel])
async def get_ai_articles_by_query_ids(
    ids: List[int] = Query(..., description="IDs de análisis de IA a consultar")
):
    """
    Obtiene artículos procesados por IA basándose en IDs.
    Equivalente a GET /aiArticlesQuery del servicio original.
    """
    if not ids:
        raise HTTPException(status_code=400, detail="Lista de IDs no puede estar vacía")
    
    return await service.get_ai_articles_by_ids(ids)

@router.get("/{article_id}", response_model=ArticleResponseModel)
async def get_article_by_id(
    article_id: int
):
    """
    Obtiene un artículo específico por ID.
    Equivalente a GET /{article_id} del servicio original.
    """
    return await service.get_article_by_id(article_id)

# Endpoints legacy/alternativos (mantener por compatibilidad)
@router.get("/search", response_model=List[ArticleResponseModel])
async def search_articles_legacy(
    query: str = Query(...),
    page: int = Query(1, ge=1),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    """
    Endpoint de búsqueda legacy (mantener por compatibilidad).
    """
    return await service.search_articles_by_text(
        query=query, 
        page=page, 
        start_date=start_date, 
        end_date=end_date
    )

@router.get("/pages", response_model=ArticlePageCountResponseModel)
async def article_pages_legacy(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    """
    Endpoint de páginas legacy (mantener por compatibilidad).
    """
    return await service.get_article_pages(
        start_date=start_date, 
        end_date=end_date
    )

@router.get("/ai", response_model=List[ArticleAIResponseModel])
async def articles_ai_legacy(
    ids: List[int] = Query(...)
):
    """
    Endpoint de IA legacy (mantener por compatibilidad).
    """
    return await service.get_ai_articles_by_ids(ids)

@router.post("/ai", response_model=List[ArticleAIResponseModel])
async def articles_ai_post(
    request: AIRequestIDs
):
    """
    Versión POST para obtener artículos de IA (para listas grandes de IDs).
    """
    return await service.get_ai_articles_by_ids(request.ids)