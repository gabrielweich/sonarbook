from fastapi import APIRouter

from src.api.controllers import activity_log, post, user


def include_routers(api: APIRouter):
    api.include_router(user.router, prefix="/users", tags=["user"])
    api.include_router(post.router, prefix="/posts", tags=["post"])
    api.include_router(activity_log.router, prefix="/activity-logs", tags=["activity_log"])
