from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    # JWT
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"

    APPLICATIONS_MODULE: str = "applications"
    APPLICATIONS: list = ["users"]

    class Config:
        env_file = ".env"
        from_attributes = True

settings = Settings()