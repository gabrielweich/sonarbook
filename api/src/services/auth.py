from datetime import datetime, timedelta
from typing import Dict

from jose import jwt

from src.config.settings import settings
from src.db import mappings
from src.services.exceptions.exceptions import ErrorCodeEnum, UnauthorizedError


class AuthService:
    def __init__(self, pwd_context):
        self.pwd_context = pwd_context

    def _encode_data(self, data, expiration, algorithm):
        key = settings.PRIVATE_KEY.get_secret_value()
        to_encode = data.copy()
        expire = datetime.utcnow() + expiration
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def create_access_token(self, user_id):
        data = {"sub": str(user_id)}
        expiration = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRES)
        return self._encode_data(data, expiration=expiration, algorithm=settings.ACCESS_ALGORITHM)

    def create_refresh_token(self, user_id):
        data = {"sub": str(user_id)}
        expiration = timedelta(seconds=settings.REFRESH_TOKEN_EXPIRES)
        return self._encode_data(data, expiration=expiration, algorithm=settings.REFRESH_ALGORITHM)

    def auth(self, token: str, key: str, algorithm: str) -> Dict:
        credentials_exception = UnauthorizedError(
            code=ErrorCodeEnum.INVALID_CREDENTIALS,
            message="Could not validate credentials",
        )

        try:
            payload = jwt.decode(token, key=key, algorithms=[algorithm])
            user_id: str = payload.get("sub")

            if user_id is None:
                raise credentials_exception
            return user_id
        except jwt.JWTError:
            raise credentials_exception

    def validate_user(self, user: mappings.User) -> None:
        if not user:
            raise UnauthorizedError(
                code=ErrorCodeEnum.INVALID_CREDENTIALS,
                message="Incorrect username or password",
            )

        if not user.is_active:
            raise UnauthorizedError(
                code=ErrorCodeEnum.INVALID_CREDENTIALS,
                message="User disabled",
            )
