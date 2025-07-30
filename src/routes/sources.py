from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from src.dependencies.auth import require_token
from src.services.axioma_service import AxiomaService
from src.schema.sources_models import SourceResponseModel, CountryResponseModel

router = APIRouter(
    prefix="/gateway/sources", 
    tags=["Sources"], 
    dependencies=[Depends(require_token)]
)

service = AxiomaService()

@router.get("/get_all", response_model=List[SourceResponseModel])
async def get_all_sources():
    """
    Obtiene todas las fuentes de noticias disponibles.
    Equivalente a GET /get_all del servicio original.
    """
    return await service.get_sources()

@router.get("/search", response_model=List[SourceResponseModel])
async def search_sources(
    name: Optional[str] = Query(default=None, description="Search sources by name"),
    country: Optional[str] = Query(default=None, description="Search sources by country name")
):
    """
    Busca fuentes por nombre o país.
    Equivalente a GET /search del servicio original.
    """
    # Validación igual que en el servicio original
    if (name and country) or (not name and not country):
        raise HTTPException(
            status_code=400,
            detail="You must provide exactly one query parameter: either 'name' or 'country'."
        )
    
    return await service.search_sources(name=name, country=country)

@router.get("/countries", response_model=List[CountryResponseModel])
async def get_all_countries():
    """
    Obtiene todos los países disponibles.
    Equivalente a GET /countries del servicio original.
    """
    return await service.get_countries()

@router.get("/countries/search", response_model=List[CountryResponseModel])
async def search_country_by_name(
    name: str = Query(..., description="Country name to search for")
):
    """
    Busca países por nombre.
    Equivalente a GET /countries/search del servicio original.
    """
    result = await service.search_country(name)
    
    # Verificar si no hay resultados (como en el servicio original)
    if not result or (isinstance(result, list) and len(result) == 0):
        raise HTTPException(status_code=404, detail="No results found.")
    
    return result

@router.get("/countries/{country_id}", response_model=CountryResponseModel)
async def get_country_by_id(country_id: int):
    """
    Obtiene un país específico por su ID.
    """
    try:
        country = await service.get_country_by_id(country_id)
        if not country:
            raise HTTPException(status_code=404, detail="Country not found.")
        return country
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/{source_id}", response_model=SourceResponseModel)
async def get_source_by_id(source_id: int):
    """
    Obtiene una fuente específica por su ID.
    """
    try:
        source = await service.get_source_by_id(source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found.")
        return source
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")