from sqlalchemy import Column, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.mappings.base import BaseModel


class ActivityLog(BaseModel):
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", lazy="noload")
    post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"), nullable=False)
    post = relationship("Post", lazy="noload")
    interaction_type = Column(String, nullable=False)

    __table_args__ = (
        Index(
            "activity_log_user_post_like_idx",
            user_id,
            post_id,
            unique=True,
            postgresql_where=(interaction_type == "like"),
        ),
        Index("activity_log_post_interaction_idx", post_id, interaction_type, unique=False),
    )
