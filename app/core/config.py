from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/postgres"
    API_KEY: str = "SECRET_API_KEY"

settings = Settings()