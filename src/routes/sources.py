from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from src.dependencies.auth import require_token
from src.schema.response_schema import SourceResponse
from src.services.axioma_service import AxiomaService

router = APIRouter(prefix="/gateway/sources", tags=["sources"], dependencies=[Depends(require_token)] )
service = AxiomaService()

@router.get("", )
async def get_sources(token: str = Depends(require_token)):
    return await service.get_sources(token)

@router.get("/search")
async def search_sources(
    token: str = Depends(require_token),
    name: Optional[str] = Query(None),
    country: Optional[str] = Query(None)
):
    return await service.search_sources(token, name=name, country=country)

@router.get("/countries")
async def countries(token: str = Depends(require_token)):
    return await service.get_countries(token)

@router.get("/countries/search")
async def search_country(
    name: str,
    token: str = Depends(require_token)
):
    return await service.search_country(token, name)