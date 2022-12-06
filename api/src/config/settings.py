import urllib.parse
from typing import List, Optional

from pydantic import BaseSettings, PostgresDsn, SecretStr, root_validator


class Settings(BaseSettings):
    PORT: int = 8000

    POSTGRES_HOST: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    DATABASE_URL: Optional[str] = None

    ALLOWED_HOSTS: List[str] = ["*"]

    ACCESS_ALGORITHM: str = "RS256"
    REFRESH_ALGORITHM: str = "HS256"

    PUBLIC_KEY: str
    PRIVATE_KEY: SecretStr

    ACCESS_TOKEN_EXPIRES: int = 10 * 60  # 10 minutes
    REFRESH_TOKEN_EXPIRES: int = 30 * 24 * 60 * 60  # 30 days

    @root_validator
    def compute_allowed_hosts(cls, values):
        allowed_hosts = values.get("ALLOWED_HOSTS")
        if isinstance(allowed_hosts, str):
            values["ALLOWED_HOSTS"] = allowed_hosts.split(",")
        return values

    @root_validator
    def compute_database_url(cls, values):
        database_url = values.get("DATABASE_URL")
        scheme = "postgresql+asyncpg"
        if isinstance(database_url, str):
            if database_url.startswith("postgres://"):
                values["DATABASE_URL"] = database_url.replace("postgres://", f"{scheme}://", 1)
            return values

        values["DATABASE_URL"] = PostgresDsn.build(
            scheme=scheme,
            user=values.get("POSTGRES_USER"),
            port=values.get("POSTGRES_PORT", "5432"),
            password=urllib.parse.quote(values.get("POSTGRES_PASSWORD", "")),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB', '')}",
        )
        return values


settings = Settings(_env_file=".env")
