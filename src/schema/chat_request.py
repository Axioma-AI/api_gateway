from typing import Optional, List
from pydantic import BaseModel, Field


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


class MultipleArticlesChatRequest(BaseModel):
    """Request to consult about multiple articles"""
    article_ids: List[int] = Field(
        ...,
        description="List of article IDs to analyze together",
        min_length=1
    )
    user_message: str = Field(
        ...,
        description="Current user question or message about the articles",
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
                    "name": "Multiple articles summary",
                    "value": {
                        "article_ids": [123, 456, 789],
                        "user_message": "Give me a summary of these articles and identify common themes",
                        "temperature": 0.7
                    }
                },
                {
                    "name": "Multiple articles with history",
                    "value": {
                        "article_ids": [123, 456, 789],
                        "user_message": "What are the key differences between them?",
                        "history": [
                            {
                                "role": "user",
                                "content": "Give me a summary of these articles"
                            },
                            {
                                "role": "assistant",
                                "content": "These articles discuss..."
                            }
                        ],
                        "temperature": 0.7
                    }
                }
            ]
        }
