from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

# Modelos base
class SourceModel(BaseModel):
    id: int
    name: str
    logo_url: Optional[HttpUrl] = Field(None, example="https://eldeber.com.bo/logo.png")

class AICategoryModel(BaseModel):
    id: int
    lang: str
    category: Optional[str]
    category_justification: Optional[str]

class AICharacterModel(BaseModel):
    id: int
    lang: str
    name: Optional[str]
    description: Optional[str]

# Modelos de respuesta principales
class ArticleResponseModel(BaseModel):
    id: int
    source: SourceModel
    author: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    url: str
    urlToImage: Optional[str] = None
    publishedAt: str
    is_favorite: Optional[bool] = None
    language: Optional[str] = None
    analysis_ids: List[int] = []
    sentiment_category: Optional[str] = None
    sentiment_score: Optional[float] = None
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": 10234,
            "source": {"id": 5, "name": "BBC News", "logo_url": "https://bbc.com/logo.png"},
            "author": "Jane Doe",
            "title": "Economic growth shows signs of recovery",
            "description": "The latest economic data shows signs of growth...",
            "content": "The latest economic data shows signs of growth...",
            "url": "https://bbc.com/economy/growth-2024",
            "urlToImage": "https://bbc.com/images/economy-growth.jpg",
            "publishedAt": "2024-06-01T08:30:00",
            "language": "en",
            "analysis_ids": [2345],
            "sentiment_category": "NEUTRAL",
            "sentiment_score": 0.13
        }
    })

class ArticlePageCountResponseModel(BaseModel):
    total_pages: int = Field(..., example=5, description="Total number of pages available for the given date range")

class ArticleAIResponseModel(BaseModel):
    news_core_id: int
    news_ai_id: int
    lang: str
    summary: Optional[str]
    sentiment_category: Optional[str]
    sentiment_score: Optional[float]
    sentiment_analysis: Optional[str]
    country: Optional[str]
    city: Optional[str]
    structure_clarity: Optional[str]
    structure_key_data: Optional[str]
    neutrality_content: Optional[str]
    was_translated: Optional[bool]
    newsAiCategory: List[AICategoryModel]
    newsAiCharacters: List[AICharacterModel]

# Modelo para la petición de IDs de AI
class AIRequestIDs(BaseModel):
    ids: List[int]

class NewsFavoritesCoreRequest(BaseModel):
    newsCoreId: int

class UpdateFavoritesResponse(BaseModel):
    newsCoreId: int
    message: str

class ChatMessage(BaseModel):
    """Message in the conversation history"""
    role: str = Field(
        ...,
        description="Role: 'user' or 'assistant'",
        pattern="^(user|assistant)$"
    )
    content: str = Field(
        ...,
        description="Message content",
        min_length=1
    )


class ChatRequest(BaseModel):
    """Request to consult about a specific article"""
    user_message: str = Field(
        ...,
        description="Current user question or message about the article",
        min_length=1
    )
    history: Optional[List[ChatMessage]] = Field(
        None,
        description="Previous message history (optional, to continue conversation)"
    )
    temperature: float = Field(
        0.7,
        description="Temperature for generation (0.0 to 1.0)",
        ge=0.0,
        le=1.0
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "name": "First consultation",
                    "value": {
                        "user_message": "What is this article about?",
                        "temperature": 0.7
                    }
                },
                {
                    "name": "Conversation continuation",
                    "value": {
                        "user_message": "What is the economic impact?",
                        "history": [
                            {
                                "role": "user",
                                "content": "What is this article about?"
                            },
                            {
                                "role": "assistant",
                                "content": "This article is about the increase in inflation..."
                            }
                        ],
                        "temperature": 0.7
                    }
                }
            ]
        }
