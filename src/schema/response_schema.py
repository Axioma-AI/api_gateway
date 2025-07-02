from pydantic import BaseModel
from typing import List, Optional

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str

class SourceResponse(BaseModel):
    id: int
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]