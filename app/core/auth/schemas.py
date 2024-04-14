from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4


class CredentialsSchema(BaseModel):
    code: int

    class Config:
        json_schema_extra = {"example": {"code": 123456}}


class JWTToken(BaseModel):
    access_token: str
    token_type: str


class JWTTokenPayload(BaseModel):
    user_uuid: UUID4
    exp: datetime


class JWTSmsTokenPayload(JWTTokenPayload):
    created_at: datetime


class Msg(BaseModel):
    msg: str
