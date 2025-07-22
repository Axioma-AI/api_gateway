from fastapi import APIRouter, Depends, Query
from src.dependencies.auth import require_token
from src.services.axioma_service import AxiomaService

router = APIRouter(
    prefix="/gateway/interests",
    tags=["Interests"],
    dependencies=[Depends(require_token)]
)

service = AxiomaService()

@router.get("/")
async def get_interests(
    token: str = Depends(require_token)
):
    """
    Obtiene todos los interests del usuario autenticado.
    Retorna una lista de strings con los keywords de interés.
    
    Respuesta esperada:
    {
        "interests": ["technology", "sports", "music"]
    }
    """
    return await service.get_interests(token)


@router.post("/")
async def add_interest(
    keyword: str = Query(..., description="Keyword del interest a añadir", min_length=2, max_length=100),
    token: str = Depends(require_token)
):
    """
    Añade un nuevo interest al usuario autenticado.
    El keyword se guarda en minúsculas automáticamente.
    
    Parámetros:
    - keyword: String entre 2 y 100 caracteres
    
    Respuesta esperada:
    {
        "keyword": "technology",
        "message": "Interest añadido exitosamente"
    }
    """
    return await service.add_interest(keyword, token)