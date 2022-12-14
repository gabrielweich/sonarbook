from __future__ import annotations

from functools import cached_property

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.activity_log import ActivityLogRepository
from src.db.repositories.post import PostRepository
from src.db.repositories.user import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> UnitOfWork:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @cached_property
    def user(self) -> UserRepository:
        return UserRepository(self.session)

    @cached_property
    def post(self) -> PostRepository:
        return PostRepository(self.session)

    @cached_property
    def activity_log(self) -> ActivityLogRepository:
        return ActivityLogRepository(self.session)
