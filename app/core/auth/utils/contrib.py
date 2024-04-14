import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, OAuth2
from jwt import PyJWTError
from jwt.exceptions import InvalidTokenError
from starlette.status import HTTP_403_FORBIDDEN

from app.applications.users.models import SmsAuthCode, User
from app.core.auth.schemas import JWTSmsTokenPayload, JWTTokenPayload, CredentialsSchema
from app.core.auth.utils import sms_code
from app.core.auth.utils.jwt import ALGORITHM
from app.config.settings import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login/access-token")
sms_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login/send_sms_code")



async def get_sms(token: str = Security(sms_oauth)) -> Optional[SmsAuthCode]:
    try:
        payload = jwt.decode(token, settings.SMS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = JWTSmsTokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    user = await User.find_one(User.uuid==token_data.user_uuid, fetch_links=True)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.sms_auth_codes:
        raise HTTPException(status_code=404, detail="Sms session doesnt exist")

    user.sms_auth_codes.sort(key=lambda s: s.created_at, reverse=True)
    
    sms = user.sms_auth_codes[0]
    
    if sms.created_at == token_data.created_at:
        raise HTTPException(status_code=404, detail="Sms session is outdated")

    if datetime.now(timezone.utc) > token_data.exp:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Your token is expired"
        )

    return sms

async def get_current_user(token: str = Security(reusable_oauth2)) -> Optional[User]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = JWTTokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    user = await User.find_one(User.uuid==token_data.user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # if datetime.utcnow() > token_data.exp:
    #     raise HTTPException(
    #         status_code=HTTP_403_FORBIDDEN,
    #         detail="Your token is expired"
    #     )

    return user


async def get_current_admin(current_user: User = Security(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")

    return current_user



async def get_current_admin(current_user: User = Security(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")

    return current_user


async def authenticate(sms: SmsAuthCode, code: int) -> Optional[User]:
    if sms.user is None:
        return None
    
    if (sms.expires_delta + sms.created_at) < datetime.utcnow():
        return None

    verified, updated_code_hash = sms_code.verify_and_update_sms_code(str(code), sms.code_hash)

    if not verified:
        return None

    if updated_code_hash is not None:
        sms.code_hash = updated_code_hash
        await sms.save()

    return sms
