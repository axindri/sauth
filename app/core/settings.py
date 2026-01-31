from functools import cached_property

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


class AppSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="APP_")

    debug: bool = Field(default=False)


class DatabaseSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")
    database: str = Field(default="sauth")

    @cached_property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    db: int = Field(default=0)

    @cached_property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class AuthSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="AUTH_")

    secret_key: str = Field(default="sauth-secret-key-that-more-than-32-symbols", min_length=32)
    access_token_expire_seconds: int = Field(default=60 * 5, ge=1)  # 5 minutes
    refresh_token_expire_seconds: int = Field(default=60 * 60 * 24 * 30, ge=1)  # 30 days
    algorithm: str = Field(default="HS256", description="JWT algorithm")

    request_token_expire_seconds: int = Field(default=60 * 5, ge=1)  # 5 minutes


class Settings(BaseConfig):
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()


settings = Settings()
