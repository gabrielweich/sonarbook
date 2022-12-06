from uuid import UUID

from fastapi import APIRouter, Depends

import src.services.models.activity_log as app_models
from src.api.dependencies.auth import current_user
from src.api.dependencies.services import activity_log_service
from src.services.activity_log import ActivityLogService


router = APIRouter()


@router.post("", response_model=app_models.CreateActivityLogResponse, status_code=201)
async def create_activity_log(
    activity_log: app_models.CreateActivityLogRequest,
    user_id: UUID = Depends(current_user),
    service: ActivityLogService = Depends(activity_log_service),
):
    return await service.create_activity_log(user_id, activity_log)
