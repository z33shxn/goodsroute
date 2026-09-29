from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Example: postgresql+psycopg2://postgres:postgres@localhost:5432/goodsroute
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/goodsroute"
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
