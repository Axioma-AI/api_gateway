from fastapi import APIRouter, Depends
from src.schemas.auth_schema import LoginRequest, UpdateProfileRequest
from src.schemas.response_schema import TokenResponse, UserResponse
from src.dependencies.auth import require_token
from src.services.auth_service import AuthService

router = APIRouter(prefix="/gateway", tags=["auth"])
service = AuthService()

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    return await service.login(request.dict())

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    request: UpdateProfileRequest,
    token: str = Depends(require_token)
):
    return await service.update(request.dict(), token)

@router.get("/profile", response_model=UserResponse)
async def get_profile(token: str = Depends(require_token)):
    return await service.get_profile(token)