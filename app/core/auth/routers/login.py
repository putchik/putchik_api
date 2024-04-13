import aiohttp

from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends

from app.applications.users.models import SmsAuthCode, User
from app.core.auth.schemas import JWTToken, CredentialsSchema
from app.core.auth.utils.contrib import authenticate, get_current_user
from app.core.auth.utils.jwt import create_access_token
from app.config.settings import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.applications.users.schemas import BaseUser
from app.core.auth.utils.sms_code import generate_sms_auth_code, get_sms_code_hash

router = APIRouter()


@router.post("/access-token", response_model=JWTToken)
async def login_access_token(credentials: CredentialsSchema = Depends()):
    # credentials = CredentialsSchema(
    #     email=credentials.username, password=credentials.password
    # )
    user = await authenticate(credentials)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
            data={"user_uuid": str(user.uuid)}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/send_sms_code", status_code=200)
async def send_sms_code(user_in: CredentialsSchema):
    user = await User.find_one(user_in.phone_number == User.phone_number)
    if user is None:
        raise HTTPException(status_code=404, detail="User doesnt exist")

    sms_code = generate_sms_auth_code(length=6)
    cur_time = datetime.utcnow()
    sms_code_expires_delta = timedelta(seconds=settings.SMS_CODE_EXPIRE_SECONDS)
    sms = SmsAuthCode(
        user=user,
        code_hash=get_sms_code_hash(sms_code),
        created_at=cur_time,
        expires_delta=sms_code_expires_delta,
    )
    
    headers = {"Authorization": f"Bearer {settings.SMS_API_CODE}", "Content-Type": "application/json"}
    async with aiohttp.ClientSession(headers=headers) as session:
        data = {
            "number": "79346690325",
            "destination": "79858693770",
            "text": f"{sms_code}"
        }
        async with session.post(
            "https://api.exolve.ru/messaging/v1/SendSMS", json=data
        ) as r:
            # print(r.status, r.raw_headers, r.request_info)
            print(await r.json())

    await sms.save()
