from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AgentFlow"
    environment: str = "development"

    database_url: str
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str

    jwt_secret: str
    access_token_expire_minutes: int = 30

    model_encryption_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False
    )


settings = Settings()
