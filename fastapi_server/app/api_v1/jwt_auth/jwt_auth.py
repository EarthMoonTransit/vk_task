from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from app.users.schemas import UserCreate, UserBase, User
from app.users.crud import create_user
from app.auth.utils import encode_jwt
from app.db import db_helper
from pydantic import BaseModel
from loguru import logger
from .helpers import create_access_token, create_refresh_token, check_domain
from .validation import (
    get_current_auth_user_for_refresh,
    get_current_token_payload,
    get_current_active_auth_user,
)
from app.core.helpers import Env, Domain

# from .schemas import TokenInfo

http_bearer = HTTPBearer(auto_error=False)
# oauth2 = OAuth2PasswordBearer(
#    tokenUrl="/api/v1/jwt/login",
# )

router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


def validate_auth_user(
    login: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    pass


@router.post("/register/", response_model=User)
async def auth_user_issue_jwt(
    user: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user.domain = Domain.master
    return await create_user(session, user)


@router.post("/login/", response_model=TokenInfo)
async def auth_user_jwt(user: UserBase):
    if check_domain(user):
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user.login} is slave"
    )


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_refresh_jwt(
    user: UserCreate = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


@router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserBase = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "login": user.email,
        "logged_in_at": iat,
    }
