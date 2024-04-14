from beanie import Document, Link, BackLink
from pydantic import UUID4, Field
from datetime import datetime, timedelta
from typing import List, Optional


class User(Document):
    uuid: UUID4
    fullname: Optional[str] = None
    phone_number: str
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    sms_auth_codes: List[BackLink["SmsAuthCode"]] = Field(original_field="user")

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "phone_number": "+79858693770",
                "password": "3xt3m#",
            }
        }

    class Settings:
        name = "users"


class SmsAuthCode(Document):
    code_hash: str
    created_at: datetime
    user: Link[User]
    expires_delta: timedelta

    class Settings:
        name = "sms_auth_codes"
