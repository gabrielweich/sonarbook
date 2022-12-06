from uuid import UUID

from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

import src.services.models.user as app_models
from src.api.dependencies.auth import current_user
from src.api.dependencies.services import user_service
from src.services.user import UserService


router = APIRouter()


@router.post("", response_model=app_models.CreateUserResponse, status_code=201)
async def create_user(user: app_models.CreateUserRequest, service: UserService = Depends(user_service)):
    return await service.create_user(user)


@router.post("/token", response_model=app_models.LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(user_service)
):
    result = await service.login(form_data.username, form_data.password)
    return result


@router.post("/refresh", response_model=app_models.LoginResponse)
async def refresh(
    refresh_token: str = Form(...),
    service: UserService = Depends(user_service),
):
    return await service.refresh_token(refresh_token)


@router.get("/me", response_model=app_models.GetUserResponse)
async def get_own_user(user_id: UUID = Depends(current_user), service: UserService = Depends(user_service)):
    return await service.get_user(user_id)


@router.get("/stats", response_model=app_models.GetStatsResponse)
async def get_users_stats(service: UserService = Depends(user_service)):
    return await service.get_stats()
