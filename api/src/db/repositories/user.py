from typing import Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.mappings.user import User
from src.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_username(self, username) -> Optional[User]:
        query = sa.select(User).where(User.username == username)
        res = await self.db.execute(query)
        return res.scalar()
