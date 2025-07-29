from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    DB_USER: str = ""
    DB_PASS: str = "postgres"
    SECRET_KEY: str
    ALGORITHM: str

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_HOST: str = "localhost"
    TEST_DB_PORT: int = 5432
    TEST_DB_NAME: str = "test_booking_db"
    TEST_DB_USER: str = ""
    TEST_DB_PASS: str = "postgres"

    @property
    def TEST_DATABASE_URL_ASYNC(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    SMTP_USER: str
    SMTP_PASS: str
    SMTP_HOST: str
    SMTP_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
