from uuid import UUID

from fastapi import APIRouter, Depends

import src.services.models.post as app_models
from src.api.dependencies.auth import current_user
from src.api.dependencies.common import PaginationParams
from src.api.dependencies.services import post_service
from src.services.models.common import Paginated
from src.services.post import PostService


router = APIRouter()


@router.post("", response_model=app_models.CreatePostResponse, status_code=201)
async def create_post(post: app_models.CreatePostRequest, service: PostService = Depends(post_service)):
    return await service.create_post(post)


@router.get("/{post_id}", response_model=app_models.GetPostResponse)
async def get_post(
    post_id: UUID, user_id: UUID = Depends(current_user), service: PostService = Depends(post_service)
):
    return await service.get_post(user_id, post_id)


@router.get("", response_model=Paginated[app_models.ListPostResponse])
async def list_posts(
    params: PaginationParams = Depends(),
    service: PostService = Depends(post_service),
):
    return await service.list_posts(params.page, params.page_size, params.sort)
