from __future__ import annotations

from fastapi import APIRouter, Depends, status
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from src.dependencies.auth import require_token
from src.services.auth_service import AuthService

router = APIRouter(
    prefix="/gateway/subscriptions",
    tags=["Subscriptions"],
    dependencies=[Depends(require_token)]
)

service = AuthService()

# Request DTOs (camelCase, iguales a TS)
class CreateSubscriptionDTO(BaseModel):
    productId: str = Field(..., description="ID del producto/plan del store")
    platform: str = Field(..., description="Plataforma (android/ios) o proveedor (google_play/apple)")
    receiptData: Optional[Dict[str, Any]] = Field(None, description="Recibo crudo del store (opcional)")

    class Config:
        json_schema_extra = {
            "example": {
                "productId": "pro_plan_monthly",
                "platform": "android",
                "receiptData": {
                    "purchaseToken": "abc123",
                    "productId": "pro_plan_monthly",
                    "packageName": "com.example.app"
                }
            }
        }


class VerifyReceiptDTO(BaseModel):
    receiptData: Dict[str, Any] = Field(..., description="Recibo crudo del store")

    class Config:
        json_schema_extra = {
            "example": {
                "receiptData": {
                    "purchaseToken": "abc123",
                    "productId": "pro_plan_monthly",
                    "packageName": "com.example.app",
                    "expiryTimeMillis": "1761000000000"
                }
            }
        }


# Response Models (alineados a lo que típicamente devuelve tu Express/Prisma)
class SubscriptionModel(BaseModel):
    id: Optional[int] = Field(None, description="ID interno (Prisma)")
    subscriptionId: Optional[str] = Field(None, description="UUID público de la suscripción")
    userId: Optional[int] = Field(None, description="ID del usuario")
    tier: Optional[str] = Field(None, description="Nivel de suscripción (ej. PRO, ANALYST, FREE)")
    status: Optional[str] = Field(None, description="Estado (ACTIVE, CANCELLED, EXPIRED)")
    startDate: Optional[str] = Field(None, description="Inicio ISO8601")
    endDate: Optional[str] = Field(None, description="Fin ISO8601")
    autoRenew: Optional[bool] = Field(None, description="Auto renovación")
    platform: Optional[str] = Field(None, description="android / ios")
    productId: Optional[str] = Field(None, description="Product ID del store")
    provider: Optional[str] = Field(None, description="google_play / apple")
    receiptData: Optional[Dict[str, Any]] = Field(None, description="JSON del recibo")
    createdAt: Optional[str] = Field(None, description="Creación ISO8601")
    updatedAt: Optional[str] = Field(None, description="Actualización ISO8601")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 42,
                "subscriptionId": "9f9b6f5f-8c8d-4b1e-bc22-8b7a9d6f1e21",
                "userId": 7,
                "tier": "PRO",
                "status": "ACTIVE",
                "startDate": "2025-08-19T10:00:00Z",
                "endDate": "2025-09-18T10:00:00Z",
                "autoRenew": True,
                "platform": "android",
                "productId": "pro_plan_monthly",
                "provider": "google_play",
                "receiptData": {"purchaseToken": "abc123"},
                "createdAt": "2025-08-19T10:00:00Z",
                "updatedAt": "2025-08-19T10:00:00Z"
            }
        }


class VerifySubscriptionResponse(BaseModel):
    hasSubscription: bool = Field(..., description="Si el usuario tiene suscripción activa")
    subscription: Optional[SubscriptionModel] = Field(None, description="Suscripción activa (si existe)")

    class Config:
        json_schema_extra = {
            "example": {
                "hasSubscription": True,
                "subscription": SubscriptionModel.Config.json_schema_extra["example"]
            }
        }


class CancelSubscriptionResponse(BaseModel):
    message: str = Field(..., example="Suscripción cancelada")
    subscriptionId: Optional[str] = Field(None, description="UUID público de la suscripción cancelada")

    class Config:
        json_schema_extra = {"example": {"message": "Suscripción cancelada", "subscriptionId": "9f9b6f5f-8c8d-4b1e-bc22-8b7a9d6f1e21"}}


# =========================
# Routes (proxy a Express)
# =========================

@router.post(
    "",
    summary="Create or update subscription",
    response_model=SubscriptionModel,
    status_code=status.HTTP_200_OK,
)
async def create_subscription(
    payload: CreateSubscriptionDTO,
    token: str = Depends(require_token),
):
    """
    Proxy → **POST /api/v1/subscriptions** (Express)
    Body **camelCase** (productId, platform, receiptData).
    Token: **Authorization: Bearer**.
    """
    # Se reenvía tal cual lo espera Express:
    data = payload.model_dump()
    return await service.create_subscription(token, data)


@router.get(
    "/verify",
    summary="Verify current subscription",
    response_model=VerifySubscriptionResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_subscription(
    token: str = Depends(require_token),
):
    """
    Proxy → **GET /api/v1/subscriptions/verify** (Express)
    """
    return await service.verify_subscription(token)


@router.post(
    "/cancel",
    summary="Cancel active subscription",
    response_model=CancelSubscriptionResponse,
    status_code=status.HTTP_200_OK,
)
async def cancel_subscription(
    token: str = Depends(require_token),
):
    """
    Proxy → **POST /api/v1/subscriptions/cancel** (Express)
    """
    return await service.cancel_subscription(token)


@router.post(
    "/verify-receipt",
    summary="Verify store receipt and upsert subscription",
    response_model=SubscriptionModel,
    status_code=status.HTTP_200_OK,
)
async def verify_receipt(
    payload: CreateSubscriptionDTO | VerifyReceiptDTO,
    token: str = Depends(require_token),
):
    """
    Proxy → **POST /api/v1/subscriptions/verify-receipt** (Express)

    Tu Express espera (en `verifyReceipt`) un body con:
    - `productId` (string)
    - `platform`  (string)
    - `receiptData` (object)

    Si tu cliente solo envía `{ receiptData }`, asegúrate de que el
    API Gateway valide/complete `productId`/`platform` si son obligatorios en Express.
    Aquí, si vienen, se reenvían tal cual.
    """
    # Si recibimos el CreateSubscriptionDTO, lo usamos completo; si es VerifyReceiptDTO, solo reenviamos receiptData.
    body: Dict[str, Any] = payload.model_dump()
    # En caso de que quieras forzar shape mínimo:
    # if "receiptData" not in body: raise HTTPException(422, "receiptData is required")
    return await service.verify_receipt(token, body)
