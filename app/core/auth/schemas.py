from typing import Optional

from pydantic import BaseModel, UUID4


class CredentialsSchema(BaseModel):
    phone_number: str
    code: int

    class Config:
        json_schema_extra = {
            "example": {"phone_number": "+79858693770", "code": 123456}
        }


class JWTToken(BaseModel):
    access_token: str
    token_type: str


class JWTTokenData(BaseModel):
    mail: str = None


class JWTTokenPayload(BaseModel):
    user_uuid: UUID4 = None


class Msg(BaseModel):
    msg: str
