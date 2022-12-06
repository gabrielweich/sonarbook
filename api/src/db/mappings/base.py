import re

import sqlalchemy as sa
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy.sql import func


def camel_to_snake(name: str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


@declarative_mixin
class TableNameMixin:
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)


@as_declarative()
class BaseModel(TableNameMixin):
    id = Column(UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
