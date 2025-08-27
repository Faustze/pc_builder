from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DEBUG: bool | None
    SECRET_KEY: str | None

    FLASK_APP: str | None
    FLASK_ENV: str | None

    DB_HOST: str | None
    DB_PORT: int | None
    DB_USER: str | None
    DB_PASS: str | None
    DB_NAME: str | None

    USE_ALEMBIC: bool = False

    @property
    def database_url_psycopg2(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=str(env_path), env_file_encoding="utf-8")


settings = Settings()
