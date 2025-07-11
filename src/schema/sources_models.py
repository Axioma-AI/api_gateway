from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class SourceResponseModel(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="El Deber")
    url: Optional[HttpUrl] = Field(None, example="https://eldeber.com.bo")
    logo_url: Optional[HttpUrl] = Field(None, example="https://eldeber.com.bo/logo.png")
    description: Optional[str] = Field(None, example="Periódico boliviano con noticias actualizadas")
    country_name: Optional[str] = Field(None, example="Bolivia")

    class Config:
        orm_mode = True

class CountryResponseModel(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Bolivia")
    code: str = Field(..., example="BOL")
    iso2_code: Optional[str] = Field(None, example="BO")
    iso3_code: Optional[str] = Field(None, example="BOL")
    primary_language: Optional[str] = Field(None, example="Spanish")

    class Config:
        orm_mode = True