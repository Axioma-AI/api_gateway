from __future__ import annotations

from fastapi import APIRouter, Query, Body, status
from typing import Dict, Any, Optional
from schema.suscriptions_models import CreateSubscriptionRequest
from src.services.auth_service import AuthService

router = APIRouter(
    prefix="/gateway/subscriptions",
    tags=["Subscriptions"],
)

service = AuthService()

@router.post(
    "",
    summary="Create or update subscription (proxy)",
    status_code=status.HTTP_200_OK,
)
async def create_subscription(
    payload: CreateSubscriptionRequest,
    token: str = Query(..., description="User authentication token"),
):
    """
    Proxy → POST /api/v1/subscriptions (destino)
    - Gateway recibe token por query; lo reenvía por query al destino.
    - Reenvía el body tal cual.
    """
    return await service.create_subscription(token, payload)

@router.get(
    "/verify",
    summary="Verify current subscription (GET, proxy)",
    status_code=status.HTTP_200_OK,
)
async def verify_subscription_get(
    token: str = Query(..., description="User authentication token"),
):
    """
    Proxy → GET /api/v1/subscriptions/verify (destino)
    - Token por query.
    """
    return await service.verify_subscription(token)

@router.post(
    "/verify",
    summary="Verify current subscription (POST, proxy)",
    status_code=status.HTTP_200_OK,
)
async def verify_subscription_post(
    token: str = Query(..., description="User authentication token"),
    body: Optional[Dict[str, Any]] = Body(None),
):
    """
    Proxy → POST /api/v1/subscriptions/verify (destino)
    - El destino espera `{"token": "<...>"}` en el body.
    - El gateway **recibe** token por query y **construye** el body esperado.
    - Cualquier body entrante se ignora y se fuerza {"token": token}.
    """
    return await service.verify_subscription_post(token)

@router.post(
    "/cancel",
    summary="Cancel active subscription (proxy)",
    status_code=status.HTTP_200_OK,
)
async def cancel_subscription(
    token: str = Query(..., description="User authentication token"),
):
    """
    Proxy → POST /api/v1/subscriptions/cancel (destino)
    - Token por query.
    """
    return await service.cancel_subscription(token)

@router.post(
    "/verify-receipt",
    summary="Verify store receipt and upsert subscription (proxy)",
    status_code=status.HTTP_200_OK,
)
async def verify_receipt(
    payload: Dict[str, Any] = Body(...),
    token: str = Query(..., description="User authentication token"),
):
    """
    Proxy → POST /api/v1/subscriptions/verify-receipt (destino)
    - Token por query.
    - Reenvía el body tal cual (receiptData/platform/productId, etc.).
    """
    return await service.verify_receipt(token, payload)
