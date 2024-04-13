from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr, UUID4, validator
from pydantic_extra_types.phone_numbers import PhoneNumber

import uuid
from typing import Optional


class BaseProperties(BaseModel):
    @validator("uuid", pre=True, always=True, check_fields=False)
    def default_hashed_id(cls, v):
        return v or uuid.uuid4()


class BaseUser(BaseProperties):
    uuid: UUID4 = None
    phone_number: str
    is_admin: Optional[bool] = False


class BaseUserCreate(BaseProperties):
    uuid: Optional[UUID4] = None
    phone_number: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+79858693770",
            }
        }
        


class BaseUserUpdate(BaseProperties):
    password: Optional[str]
    phone_number: Optional[EmailStr]
    
    
class BaseUserUpdate(BaseProperties):
    password: Optional[str]
    phone_number: Optional[EmailStr]


class BaseUserDB(BaseUser):
    uuid: UUID4
    password_hash: str

    class Config:
        from_attributes = True


class BaseUserOut(BaseUser):
    uuid: UUID4
    phone_number: str

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "phone_number": "+79858693770",
            }
        }