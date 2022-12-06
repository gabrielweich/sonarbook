from sqlalchemy.ext.asyncio import AsyncSession

from src.db.mappings.post import Post
from src.db.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Post)
