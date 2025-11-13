from pydantic import BaseModel, ConfigDict, Field
from typing import List

class NewsHistoryModel(BaseModel):
    date: str
    news_count: int

class NewsPerceptionModel(BaseModel):
    date: str
    positive_sentiment_score: float
    negative_sentiment_score: float

class GeneralPerceptionModel(BaseModel):
    positive_sentiment_score: float
    negative_sentiment_score: float

class AnalysisResponseModel(BaseModel):
    source_query: str  # Término de búsqueda utilizado
    news_history: List[NewsHistoryModel]  # Historial de noticias por fecha sin segmentación por fuente
    news_perception: List[NewsPerceptionModel]  # Percepción de noticias general
    news_count: int  # Número total de noticias
    sources_count: int  # Número de fuentes únicas
    historic_interval: int  # Intervalo histórico
    historic_interval_unit: str  # Unidad del intervalo histórico (days, weeks, months, years)
    general_perception: GeneralPerceptionModel  # Percepción general

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "source_query": "ganaderia",
            "news_history": [
                {"date": "2024-02-15", "news_count": 15},
                {"date": "2024-04-02", "news_count": 20}
            ],
            "news_perception": [
                {
                    "date": "2024-02-15",
                    "positive_sentiment_score": 0.5,
                    "negative_sentiment_score": 0.3
                },
                {
                    "date": "2024-04-02",
                    "positive_sentiment_score": 0.7,
                    "negative_sentiment_score": 0.2
                }
            ],
            "news_count": 35,
            "sources_count": 3,
            "historic_interval": 9,
            "historic_interval_unit": "months",
            "general_perception": {
                "positive_sentiment_score": 0.6,
                "negative_sentiment_score": 0.4
            }
        }
    })

class ErrorResponseModel(BaseModel):
    detail: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "detail": "Invalid request. Query parameter is missing."
        }
    })

class SentimentCountsModel(BaseModel):
    very_positive: int = Field(0, description="Count VERY_POSITIVE")
    positive: int = Field(0, description="Count POSITIVE")
    neutral: int = Field(0, description="Count NEUTRAL")
    negative: int = Field(0, description="Count NEGATIVE")
    very_negative: int = Field(0, description="Count VERY_NEGATIVE")
    unknown: int = Field(0, description="Count UNKNOWN")


class DaySentimentResponseModel(BaseModel):
    date: str
    sentiment_counts: SentimentCountsModel
    total_news: int
    positive_sentiment_score: float
    negative_sentiment_score: float

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "date": "2025-11-12",
            "sentiment_counts": {
                "very_positive": 5,
                "positive": 20,
                "neutral": 15,
                "negative": 8,
                "very_negative": 2,
                "unknown": 1
            },
            "total_news": 51,
            "positive_sentiment_score": 0.61,
            "negative_sentiment_score": 0.39
        }
    })


class MonthSentimentResponseModel(BaseModel):
    month: str  # Formato YYYY-MM
    sentiment_counts: SentimentCountsModel
    total_news: int
    positive_sentiment_score: float
    negative_sentiment_score: float

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "month": "2025-11",
            "sentiment_counts": {
                "very_positive": 30,
                "positive": 120,
                "neutral": 90,
                "negative": 60,
                "very_negative": 25,
                "unknown": 10
            },
            "total_news": 335,
            "positive_sentiment_score": 0.57,
            "negative_sentiment_score": 0.43
        }
    })


class YearMonthSentimentModel(BaseModel):
    month: str  # Formato YYYY-MM
    sentiment_counts: SentimentCountsModel
    total_news: int
    positive_sentiment_score: float
    negative_sentiment_score: float


class YearSentimentResponseModel(BaseModel):
    year: int
    months: List[YearMonthSentimentModel]

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "year": 2025,
            "months": [
                {
                    "month": "2025-01",
                    "sentiment_counts": {
                        "very_positive": 12,
                        "positive": 45,
                        "neutral": 38,
                        "negative": 22,
                        "very_negative": 9,
                        "unknown": 4
                    },
                    "total_news": 130,
                    "positive_sentiment_score": 0.62,
                    "negative_sentiment_score": 0.38
                }
            ]
        }
    })
