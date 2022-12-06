from sqlalchemy import Boolean, Column, String

from src.db.mappings.base import BaseModel


class User(BaseModel):
    is_active = Column(Boolean, default=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
