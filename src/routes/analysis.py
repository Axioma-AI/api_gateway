from fastapi import APIRouter, Depends, Query
from typing import Union, Optional

from src.dependencies.auth import require_token
from src.services.axioma_service import AxiomaService
from src.schema.response_analysis_models import AnalysisResponseModel, DaySentimentResponseModel, ErrorResponseModel, MonthSentimentResponseModel, YearSentimentResponseModel

router = APIRouter(
    prefix="/gateway/analysis",
    tags=["Analysis"],
)

service = AxiomaService()

# Respuestas para el análisis general
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

# Respuestas para data-analysis/sentiments
data_analysis_sentiments_responses = {
    200: {
        "description": "Conteos de noticias por sentimiento",
        "model": Union[
            DaySentimentResponseModel,
            MonthSentimentResponseModel,
            YearSentimentResponseModel,
        ],
    },
    400: {
        "description": "Parámetros inválidos",
        "model": ErrorResponseModel,
    },
    500: {
        "description": "Error interno del servidor",
        "model": ErrorResponseModel,
    },
}

# =====================================================================
# ANALYSIS: VERSION PROTEGIDA
# =====================================================================
@router.get(
    "/",
    response_model=AnalysisResponseModel,
    responses=analysis_responses,
    summary="[Protegido] Análisis de sentimientos de noticias",
    description="Realiza un análisis de sentimientos de noticias basado en una "
                "consulta de texto y un rango de tiempo específico. Requiere token."
)
async def get_analysis_protected(
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
    token: str = Depends(require_token),
):
    """
    Endpoint PROTEGIDO para realizar análisis de sentimientos de noticias.
    """
    return await service.get_analysis(
        query=query,
        interval=interval,
        unit=unit,
    )

# =====================================================================
# ANALYSIS: VERSION PÚBLICA (SIN PROTECCIÓN)
# =====================================================================
@router.get(
    "/public",
    response_model=AnalysisResponseModel,
    responses=analysis_responses,
    summary="[Público] Análisis de sentimientos de noticias",
    description="Realiza un análisis de sentimientos de noticias basado en una "
                "consulta de texto y un rango de tiempo específico. NO requiere token."
)
async def get_analysis_public(
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
):
    """
    Endpoint PÚBLICO para realizar análisis de sentimientos de noticias.
    """
    return await service.get_analysis(
        query=query,
        interval=interval,
        unit=unit,
    )

# =====================================================================
# DATA-ANALYSIS / SENTIMENTS: VERSION PROTEGIDA
# =====================================================================
@router.get(
    "/data-analysis/sentiments",
    response_model=Union[
        DaySentimentResponseModel,
        MonthSentimentResponseModel,
        YearSentimentResponseModel,
    ],
    responses=data_analysis_sentiments_responses,
    summary="[Protegido] Conteo de noticias por sentimiento",
    description=(
        "Devuelve conteos de noticias por sentimiento con filtros por día (dd/mm/yyyy), "
        "mes (mm/yyyy) o año (yyyy). Para año, incluye promedio positivo/negativo por mes. "
        "Requiere token."
    ),
)
async def get_sentiment_counts_data_analysis_protected(
    scope: str = Query(
        ...,
        description="Nivel de agregación: day, month o year",
        regex="^(day|month|year)$"
    ),
    value: Optional[str] = Query(
        default=None,
        description=(
            "Valor del filtro. Formatos: day → dd/mm/yyyy, month → mm/yyyy, year → yyyy. "
            "Si no se envía, se usa la fecha actual."
        ),
    ),
    query: str = Query(
        ...,
        description="Palabra clave para buscar en las noticias (obligatoria)",
        min_length=1,
        max_length=100,
    ),
    token: str = Depends(require_token),
):
    """
    Endpoint PROTEGIDO para data-analysis/sentiments.
    """
    return await service.get_sentiment_counts_data_analysis(
        scope=scope,
        value=value,
        query=query,
    )

# =====================================================================
# DATA-ANALYSIS / SENTIMENTS: VERSION PÚBLICA
# =====================================================================
@router.get(
    "/public/data-analysis/sentiments",
    response_model=Union[
        DaySentimentResponseModel,
        MonthSentimentResponseModel,
        YearSentimentResponseModel,
    ],
    responses=data_analysis_sentiments_responses,
    summary="[Público] Conteo de noticias por sentimiento",
    description=(
        "Devuelve conteos de noticias por sentimiento con filtros por día (dd/mm/yyyy), "
        "mes (mm/yyyy) o año (yyyy). Para año, incluye promedio positivo/negativo por mes. "
        "NO requiere token."
    ),
)
async def get_sentiment_counts_data_analysis_public(
    scope: str = Query(
        ...,
        description="Nivel de agregación: day, month o year",
        regex="^(day|month|year)$"
    ),
    value: Optional[str] = Query(
        default=None,
        description=(
            "Valor del filtro. Formatos: day → dd/mm/yyyy, month → mm/yyyy, year → yyyy. "
            "Si no se envía, se usa la fecha actual."
        ),
    ),
    query: str = Query(
        ...,
        description="Palabra clave para buscar en las noticias (obligatoria)",
        min_length=1,
        max_length=100,
    ),
):
    """
    Endpoint PÚBLICO para data-analysis/sentiments.
    """
    return await service.get_sentiment_counts_data_analysis(
        scope=scope,
        value=value,
        query=query,
    )
