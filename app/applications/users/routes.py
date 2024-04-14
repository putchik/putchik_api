from datetime import timedelta

from pydantic import UUID4

from app.core.auth.utils.contrib import get_current_admin, get_current_user
from app.core.auth.utils.password import get_password_hash
from app.core.auth.utils.sms_code import generate_sms_auth_code

from app.applications.users.models import User
from app.applications.users.schemas import BaseUserOut, BaseUserCreate, BaseUserUpdate

from typing import List

from fastapi import APIRouter, Depends, HTTPException

import logging


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=List[BaseUserOut], status_code=200)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
):
    """
    Retrieve users.
    """
    users = await User.all().limit(limit).offset(skip)
    return users


@router.post("/", response_model=BaseUserOut, status_code=201)
async def create_user(
    *,
    user_in: BaseUserCreate,
):
    """
    Create new user.
    """
    user = await User.find_one(User.phone_number == user_in.phone_number)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this phone number already exists",
        )

    created_user = await User(**user_in.model_dump()).create()
    return created_user


@router.patch("/me", response_model=BaseUserOut, status_code=200)
async def update_user_me(user_in: BaseUserUpdate, current_user: User = Depends(get_current_user)):
    """
    Update own user.
    """
    if user_in.password is not None:
        hashed_password = get_password_hash(user_in.password)
        current_user.hashed_password = hashed_password
    if user_in.phone_number is not None:
        current_user.phone_number = user_in.phone_number

    await current_user.save()
    return current_user


@router.get("/me", response_model=BaseUserOut, status_code=200)
def read_user_me(
    current_user: User = Depends(get_current_user),
):
    """
    Get current user.
    """
    return current_user


@router.get("/{uuid}", response_model=BaseUserOut, status_code=200)
async def read_user_by_id(
    uuid: UUID4,
    current_user: User = Depends(get_current_admin),
):
    """
    Get a specific user by uuid.
    """
    user = await User.get(uuid=uuid)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this uuid does not exist",
        )

    return user


@router.patch("/{uuid}", response_model=BaseUserOut, status_code=200)
async def update_user(
    uuid: UUID4,
    user_in: BaseUserUpdate,
    current_user: User = Depends(get_current_admin),
):
    """
    Update a user.
    """
    user = await User.get(uuid=uuid)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist",
        )
    user = await user.update_from_dict(user_in.model_dump())
    await user.save()

    return user