from uuid import UUID

from pydantic import HttpUrl

from src.services.models.base import Base


class CreatePostRequest(Base):
    image_src: HttpUrl
    title: str
    description: str


class CreatePostResponse(Base):
    id: UUID


class ListPostResponse(Base):
    id: UUID
    image_src: str
    title: str
    views_count: int
    likes_count: int


class GetPostResponse(Base):
    id: UUID
    image_src: str
    title: str
    description: str
    likes_count: int
    user_liked: bool
