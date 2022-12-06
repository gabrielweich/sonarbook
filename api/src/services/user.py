import sqlalchemy as sa

import src.services.models.user as app_models
from src.config.settings import settings
from src.db import mappings
from src.services.auth import AuthService
from src.services.base import BaseService
from src.services.exceptions.exceptions import ErrorCodeEnum, UnauthorizedError


class UserService(BaseService):
    def __init__(self, auth_service, **kwargs):
        self.auth_service: AuthService = auth_service
        super().__init__(**kwargs)

    async def create_user(self, user: app_models.CreateUserRequest):
        async with self.uow as uow:
            password = self.auth_service.hash_password(user.password.get_secret_value())
            user_dict = {**user.dict(), "password": password}

            to_create = mappings.User(**user_dict)
            created = await uow.user.create(to_create)
            return app_models.CreateUserResponse.from_orm(created)

    async def login(self, username, password):
        user = await self.uow.user.get_by_username(username)

        self.auth_service.validate_user(user)
        success = self.auth_service.verify_password(password, user.password)

        if not success:
            raise UnauthorizedError(
                code=ErrorCodeEnum.INVALID_CREDENTIALS,
                message="Incorrect username or password",
            )

        access_token = self.auth_service.create_access_token(user.id)
        refresh_token = self.auth_service.create_refresh_token(user.id)

        return app_models.LoginResponse(access_token=access_token, refresh_token=refresh_token)

    async def get_user(self, user_id):
        user = await self.uow.user.get_by_id(user_id)
        return app_models.GetUserResponse.from_orm(user)

    async def refresh_token(self, token: str):
        key = settings.PRIVATE_KEY.get_secret_value()
        user_id = self.auth_service.auth(token=token, key=key, algorithm=settings.REFRESH_ALGORITHM)
        user = await self.uow.user.get_by_id(user_id)
        self.auth_service.validate_user(user)
        access_token = self.auth_service.create_access_token(user.id)
        return app_models.LoginResponse(access_token=access_token, refresh_token=token)

    async def get_stats(self):
        query = sa.select(mappings.User).order_by(None)
        qb_count = sa.select(sa.func.count()).select_from(query)
        count = await self.uow.user.db.execute(qb_count)
        return app_models.GetStatsResponse(count=count.scalars().first())
