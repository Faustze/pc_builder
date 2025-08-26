from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()

class Settings(BaseSettings):
    DEBUG: bool = True
    SECRET_KEY: str = "secret_key"

    DB_HOST: str = "DB_HOST"
    DB_PORT: int = 5432
    DB_USER: str = "DB_USER"
    DB_PASS: str = "DB_PASS"
    DB_NAME: str = "DB_NAME"

    USE_ALEMBIC: bool = False

    @property
    def database_url_psycopg2(self):
        return (
            f"postgresql+psycopg2://"
            f"{self.DB_USER}"
            f":{self.DB_PASS}"
            f"@{self.DB_HOST}"
            f":{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
