from typing import Literal
from pydantic_settings import BaseSettings


class SettingsBD(BaseSettings):
    MODE: Literal["PROD", "DEV", "TEST"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        auth = f"{self.DB_USER}:{self.DB_PASS}"
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql+asyncpg://{auth}@{database}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def TEST_DATABASE_URL(self):
        auth = f"{self.TEST_DB_USER}:{self.TEST_DB_PASS}"
        database = f"{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        return f"postgresql+asyncpg://{auth}@{database}"

    SALT: str

    SECRET_KEY: str
    ALGORITHM: str

    SMPT_HOST: str
    SMPT_PORT: int
    SMPT_LOGIN: str
    SMPT_PASS: str
    SMPT_EMAIL: str

    class Config:
        env_file = ".env"


settings = SettingsBD()
