import random
from typing import Tuple
from passlib import pwd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_sms_auth_code(length=6):
    return random.randint(100000, 999999)


def get_sms_code_hash(code: int) -> str:
    return pwd_context.hash(str(code))


def verify_and_update_sms_code(plain_code: str, hashed_code: str) -> Tuple[bool, str]:
    return pwd_context.verify_and_update(plain_code, hashed_code)