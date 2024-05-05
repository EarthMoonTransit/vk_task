from datetime import timedelta
from app.core.models import User
from app.auth import utils as auth_utils
from app.core.app_settings import settings
from app.users.schemas import UserBase
from app.core.helpers import Env, Domain
from app.users.dependencies import user_by_login
from app.auth.utils import encode_jwt
from app.db import db_helper
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserBase) -> str:
    jwt_payload = {
        "sub": user.login,
        "username": user.login,
        "pass": user.password,
    }
    return encode_jwt(jwt_payload)


def create_refresh_token(user: UserBase) -> str:
    jwt_payload = {
        "sub": user.login,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(
            days=get_app_settings().auth_jwt.refresh_token_expire_days
        ),
    )


async def check_domain(
    user: UserBase = Depends(user_by_login),
) -> bool:
    return True if user.domain == Domain.slave else False
