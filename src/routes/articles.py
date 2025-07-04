from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from src.dependencies.auth import require_token
from src.schema.response_schema import ArticleResponse
from src.services.axioma_service import AxiomaService

router = APIRouter(
    prefix="/gateway/articles",
    tags=["articles"],
    dependencies=[Depends(require_token)]  # ✅ Se aplica a todos los endpoints
)
service = AxiomaService()

@router.get("")
async def get_articles(
    page: int = Query(1, ge=1),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    return await service.get_articles(page=page, start_date=start_date, end_date=end_date)

@router.get("/search")
async def search_articles(
    token: str = Depends(require_token),
    query: str = Query(...),
    page: int = Query(1, ge=1),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    return await service.search_articles(token, query, page=page, start_date=start_date, end_date=end_date)

@router.get("/pages")
async def article_pages(
    token: str = Depends(require_token),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    return await service.get_article_pages(token, start_date=start_date, end_date=end_date)

@router.get("/ai")
async def articles_ai(
    token: str = Depends(require_token),
    ids: List[int] = Query(...)
):
    return await service.get_ai_articles_by_ids(token, ids)

@router.get("/{article_id}")
async def article_by_id(
    article_id: int,
    token: str = Depends(require_token)
):
    return await service.get_article_by_id(token, article_id)