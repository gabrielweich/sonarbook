import sqlalchemy as sa
from sqlalchemy.orm import query_expression, undefer, with_expression

import src.services.models.post as app_models
from src.db import mappings
from src.services.base import BaseService
from src.services.exceptions.exceptions import NotFoundError
from src.services.models.common import Sort


class PostService(BaseService):
    async def create_post(self, post: app_models.CreatePostRequest):
        async with self.uow as uow:
            to_create = mappings.Post(**post.dict())
            created = await uow.post.create(to_create)
            return app_models.CreatePostResponse.from_orm(created)

    async def get_post(self, user_id, post_id):
        mappings.Post.user_liked = query_expression()
        user_liked_query = (
            sa.select()
            .where(mappings.ActivityLog.post_id == post_id)
            .where(mappings.ActivityLog.user_id == user_id)
            .where(mappings.ActivityLog.interaction_type == "like")
            .exists()
        )
        query = sa.select(mappings.Post).where(mappings.Post.id == post_id)
        query = query.options(
            undefer(mappings.Post.likes_count),
            undefer(mappings.Post.views_count),
            with_expression(mappings.Post.user_liked, user_liked_query),
        )

        post = await self.uow.post.db.execute(query)

        post = post.scalar()

        if post is None:
            raise NotFoundError("Post not found")
        return app_models.GetPostResponse.from_orm(post)

    async def list_posts(self, page: int, page_size: int, sort: Sort):
        qb = sa.select(mappings.Post).options(
            undefer(mappings.Post.likes_count), undefer(mappings.Post.views_count)
        )
        qb = self.uow.post.sort_query(qb, sort)
        return await self.uow.post.paginate_query(qb, app_models.ListPostResponse, page, page_size)
