from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    idToken: str

class UpdateProfileRequest(BaseModel):
    displayName: Optional[str] = None
    photoUrl: Optional[str] = None