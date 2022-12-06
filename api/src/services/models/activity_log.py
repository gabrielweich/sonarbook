import enum
from uuid import UUID

from src.services.models.base import Base


class InteractionTypeEnum(str, enum.Enum):
    like = "like"
    view = "view"


class CreateActivityLogRequest(Base):
    post_id: UUID
    interaction_type: InteractionTypeEnum


class CreateActivityLogResponse(Base):
    id: UUID
