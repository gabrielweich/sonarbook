from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.api.dependencies.services import AuthService, auth_service
from src.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")


def current_user(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends(auth_service)):
    user_id = auth_service.auth(token=token, key=settings.PUBLIC_KEY, algorithm=settings.ACCESS_ALGORITHM)
    return user_id
