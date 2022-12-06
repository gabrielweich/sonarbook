from fastapi import Depends
from passlib.context import CryptContext

from src.api.dependencies.common import get_uow
from src.services.activity_log import ActivityLogService
from src.services.auth import AuthService
from src.services.post import PostService
from src.services.user import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def auth_service():
    return AuthService(pwd_context=pwd_context)


def user_service(uow=Depends(get_uow), auth_service=Depends(auth_service)):
    return UserService(uow=uow, auth_service=auth_service)


def post_service(uow=Depends(get_uow)):
    return PostService(uow)


def activity_log_service(uow=Depends(get_uow)):
    return ActivityLogService(uow)
