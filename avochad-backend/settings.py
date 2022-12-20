from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgres://postgres:root@localhost:5432/avochad"
    SECRET_KEY: str = "secret"

    class Config:

        env_file = ".env"

        env_file_encoding = "utf-8"


settings = Settings()