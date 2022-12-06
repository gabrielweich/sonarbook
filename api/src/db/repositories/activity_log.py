from sqlalchemy.ext.asyncio import AsyncSession

from src.db.mappings.activity_log import ActivityLog
from src.db.repositories.base import BaseRepository


class ActivityLogRepository(BaseRepository[ActivityLog]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ActivityLog)
