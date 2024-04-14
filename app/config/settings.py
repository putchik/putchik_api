from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    # JWT
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # sms
    SMS_CODE_EXPIRE_SECONDS: int = 60
    SMS_API_CODE: str
    SMS_TOKEN_SECRET_KEY : str
    SMS_SENDER_PHONE_NUMBER: str

    # application
    APPLICATIONS_MODULE: str = "applications"
    APPLICATIONS: list = ["users"]
    
    
    class Config:
        env_file = ".env"
        from_attributes = True

settings = Settings()