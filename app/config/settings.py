from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.paths import ENV_FILE_PATH


class Settings(BaseSettings):
    SQL_ALCHEMY__DATABASE_URL: str

    JWT__SECRET_KEY: str = "SuPeR_SEcReT_keY"
    JWT__ALGORITHM: str = "HS256"
    JWT__ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, env_file_encoding="utf-8", extra="ignore")


settings = Settings()
