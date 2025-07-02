from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager

from src.routes.gateway_router import router as gateway_router
from src.config.settings import get_settings
from src.utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)

origins = ["*"]

app = FastAPI(
    title="API Gateway",
    debug=settings.debug,
    description="Gateway que enruta solicitudes a los microservicios y requiere autenticación por token.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
)

app.include_router(gateway_router)

# Swagger: agregar esquema de seguridad Bearer
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # No aplicamos seguridad global, solo se usa en rutas con Depends
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
