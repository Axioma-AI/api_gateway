from fastapi import APIRouter, Depends, Query
from src.dependencies.auth import require_token
from src.services.axioma_service import AxiomaService
from src.schema.response_analysis_models import AnalysisResponseModel, ErrorResponseModel

router = APIRouter(
    prefix="/gateway/analysis",
    tags=["Analysis"],
    dependencies=[Depends(require_token)]
)

service = AxiomaService()

# Definir las respuestas posibles para la documentación
analysis_responses = {
    200: {
        "description": "Análisis de sentimientos exitoso",
        "model": AnalysisResponseModel
    },
    400: {
        "description": "Parámetros inválidos",
        "model": ErrorResponseModel
    },
    500: {
        "description": "Error interno del servidor",
        "model": ErrorResponseModel
    }
}

@router.get(
    "/",
    response_model=AnalysisResponseModel,
    responses=analysis_responses,
    summary="Análisis de sentimientos de noticias",
    description="Realiza un análisis de sentimientos de noticias basado en una consulta de texto y un rango de tiempo específico."
)
async def get_analysis(
    query: str = Query(
        ...,
        description="Palabra clave para buscar en las noticias",
        min_length=1,
        max_length=100
    ),
    interval: int = Query(
        ...,
        description="Intervalo histórico para el análisis",
        ge=1,
        le=365
    ),
    unit: str = Query(
        ...,
        description="Unidad del intervalo (days, weeks, months, years)",
        regex="^(days|weeks|months|years)$"
    ),
    token: str = Depends(require_token)
):
    """
    Endpoint para realizar análisis de sentimientos de noticias.
    
    - **query**: Término de búsqueda para filtrar las noticias
    - **interval**: Número de unidades de tiempo hacia atrás desde hoy
    - **unit**: Unidad de tiempo (days, weeks, months, years)
    
    Retorna:
    - Historial de noticias por fecha
    - Percepción de sentimientos por fecha
    - Estadísticas generales del análisis
    - Percepción general de sentimientos
    """
    return await service.get_analysis(
        query=query,
        interval=interval,
        unit=unit
    )