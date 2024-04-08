from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr, UUID4, validator

import uuid
from typing import Optional


class BaseProperties(BaseModel):
    @validator("uuid", pre=True, always=True, check_fields=False)
    def default_hashed_id(cls, v):
        return v or uuid.uuid4()


class BaseUser(BaseProperties):
    uuid: UUID4 = None
    email: Optional[EmailStr] = None
    is_admin: Optional[bool] = False


class BaseUserCreate(BaseProperties):
    uuid: Optional[UUID4] = None
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+79858693770",
            }
        }


class BaseUserUpdate(BaseProperties):
    password: Optional[str]
    email: Optional[EmailStr]


class BaseUserDB(BaseUser):
    uuid: UUID4
    password_hash: str

    class Config:
        orm_mode = True


class BaseUserOut(BaseUser):
    uuid: UUID4
    tg_id: Optional[str]

    class Config:
        orm_mode = True

        json_schema_extra = {
            "example": {
                "phone_number": "+79858693770",
            }
        }