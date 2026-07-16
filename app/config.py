from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    rabbit_url: str = "amqp://guest:guest@localhost:5672/"


settings = Settings()
