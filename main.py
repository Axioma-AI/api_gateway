from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.routers.auth import router as auth_router
from src.routers.articles import router as articles_router
from src.routers.sources import router as sources_router
from src.config.settings import get_settings
from src.utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)

app = FastAPI(
    title="API Gateway",
    debug=settings.debug,
    description="Gateway que enruta solicitudes a los microservicios y requiere autenticación por token.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
)

app.include_router(auth_router)
app.include_router(articles_router)
app.include_router(sources_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi