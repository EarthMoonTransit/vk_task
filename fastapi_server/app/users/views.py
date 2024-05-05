from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from app.db import db_helper
from .dependencies import user_by_id
from .schemas import User, UserCreate


router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Получение всех пользователей"""
    return await crud.get_users(session=session)


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Создание пользователя"""
    return await crud.create_user(session=session, user_in=user_in)


@router.get("/{user_id}/", response_model=User)
async def get_user(
    user: User = Depends(user_by_id),
):
    """Получение пользователя по id"""
    return user
