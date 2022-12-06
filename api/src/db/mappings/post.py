import sqlalchemy as sa
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property

from src.db.mappings import ActivityLog
from src.db.mappings.base import BaseModel


class Post(BaseModel):
    id = Column(UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True)
    image_src = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    likes_count = column_property(
        sa.select(sa.func.count(ActivityLog.id))
        .where(ActivityLog.post_id == id)
        .where(ActivityLog.interaction_type == "like")
        .correlate_except(ActivityLog)
        .scalar_subquery(),
        deferred=True,
    )

    views_count = column_property(
        sa.select(sa.func.count(ActivityLog.id))
        .where(ActivityLog.post_id == id)
        .where(ActivityLog.interaction_type == "view")
        .correlate_except(ActivityLog)
        .scalar_subquery(),
        deferred=True,
    )
