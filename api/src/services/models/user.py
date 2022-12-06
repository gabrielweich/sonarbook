from uuid import UUID

from pydantic import SecretStr

from src.services.models.base import Base


class CreateUserRequest(Base):
    username: str
    password: SecretStr


class CreateUserResponse(Base):
    id: UUID


class LoginResponse(Base):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class GetUserResponse(Base):
    id: UUID
    username: str


class GetStatsResponse(Base):
    count: int
