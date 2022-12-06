from uuid import UUID

import src.services.models.activity_log as app_models
from src.db import mappings
from src.services.base import BaseService


class ActivityLogService(BaseService):
    async def create_activity_log(self, user_id: UUID, activity_log: app_models.CreateActivityLogRequest):
        async with self.uow as uow:
            data = {**activity_log.dict(), "user_id": user_id}
            to_create = mappings.ActivityLog(**data)
            created = await uow.activity_log.create(to_create)
            return app_models.CreateActivityLogResponse.from_orm(created)
