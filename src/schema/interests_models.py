from pydantic import BaseModel

class InterestsUpdateRequest(BaseModel):
    interests: list[str]