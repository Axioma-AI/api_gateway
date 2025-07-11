from fastapi import APIRouter, Depends
from src.schema.auth_models import LoginRequest, UpdateProfileRequest
from src.dependencies.auth import require_token
from src.services.auth_service import AuthService

router = APIRouter(prefix="/gateway", tags=["User"])
service = AuthService()

@router.post("/login")
async def login(request: LoginRequest):
    return await service.login(request.model_dump())

@router.put("/profile")
async def update_profile(
    request: UpdateProfileRequest,
    token: str = Depends(require_token)
):
    return await service.update(request.model_dump(), token)

@router.get("/profile")
async def get_profile(token: str = Depends(require_token)):
    return await service.get_profile(token)