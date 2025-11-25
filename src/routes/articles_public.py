from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Query, HTTPException

from src.schema.article_models import (
    ArticleResponseModel,
    ArticleAIResponseModel,
)
from src.services.axioma_service import AxiomaService

router = APIRouter(
    prefix="/gateway/articles/public",
    tags=["Articles - Public"],
)

service = AxiomaService()

# =====================================================================
# VERSIONES PÚBLICAS (SIN TOKEN)
# =====================================================================

@router.get(
    "/getArticles",
    response_model=List[ArticleResponseModel],
    summary="[Público] Obtener artículos",
    description="Obtiene artículos con paginación y filtros de fecha (proxy a Axioma).",
)
async def get_articles_public(
    page: int = Query(
        default=1,
        ge=1,
        description="Número de página (50 resultados por página)",
    ),
    start_date: Optional[date] = Query(
        default=None,
        description="Fecha de inicio en formato YYYY-MM-DD (por defecto: hoy)",
    ),
    end_date: Optional[date] = Query(
        default=None,
        description="Fecha de fin en formato YYYY-MM-DD (por defecto: hoy)",
    ),
):
    """
    Endpoint PÚBLICO equivalente a GET /getArticles del servicio original.
    """
    start_date_str = start_date.isoformat() if start_date else None
    end_date_str = end_date.isoformat() if end_date else None

    return await service.get_articles(
        page=page,
        start_date=start_date_str,
        end_date=end_date_str,
    )


@router.get(
    "/search_text",
    response_model=List[ArticleResponseModel],
    summary="[Público] Buscar artículos por texto",
    description="Busca artículos por texto en título o contenido (proxy a Axioma).",
)
async def search_articles_by_text_public(
    query: str = Query(
        ...,
        description="Texto a buscar en título o contenido (modo booleano)",
        min_length=1,
        max_length=200,
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Número de página (50 resultados por página)",
    ),
    start_date: Optional[date] = Query(
        default=None,
        description="Fecha de inicio (YYYY-MM-DD)",
    ),
    end_date: Optional[date] = Query(
        default=None,
        description="Fecha de fin (YYYY-MM-DD)",
    ),
):
    """
    Endpoint PÚBLICO equivalente a GET /search_text del servicio original.
    """
    start_date_str = start_date.isoformat() if start_date else None
    end_date_str = end_date.isoformat() if end_date else None

    return await service.search_articles_by_text(
        query=query,
        page=page,
        start_date=start_date_str,
        end_date=end_date_str,
    )


@router.get(
    "/aiArticlesQuery",
    response_model=List[ArticleAIResponseModel],
    summary="[Público] Obtener artículos IA por IDs",
    description="Obtiene artículos procesados por IA basándose en IDs (proxy a Axioma).",
)
async def get_ai_articles_by_query_ids_public(
    ids: List[int] = Query(
        ...,
        description="IDs de análisis de IA a consultar",
    ),
):
    """
    Endpoint PÚBLICO equivalente a GET /aiArticlesQuery del servicio original.
    """
    if not ids:
        raise HTTPException(
            status_code=400,
            detail="Lista de IDs no puede estar vacía",
        )

    return await service.get_ai_articles_by_ids(ids)


@router.get(
    "/{article_id}",
    response_model=ArticleResponseModel,
    summary="[Público] Obtener artículo por ID",
    description="Obtiene un artículo específico por ID (proxy a Axioma).",
)
async def get_article_by_id_public(
    article_id: int,
):
    """
    Endpoint PÚBLICO equivalente a GET /{article_id} del servicio original.
    """
    return await service.get_article_by_id(article_id)
