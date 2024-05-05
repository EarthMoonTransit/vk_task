from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status, Depends

from . import crud
from .dependencies import project_by_id
from .schemas import Project, ProjectCreate
from app.db import db_helper
from app.users.schemas import User
from app.core.helpers import Env, Domain
from app.users.dependencies import user_by_id


router = APIRouter(tags=["Projects"])


@router.post("/{project_id}/user/{user_id}")
async def acquire_lock(
    project: Project = Depends(project_by_id),
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Блокировка пользователя и связывание с Проектом"""
    now = datetime.utcnow()
    if now > user.locktime:
        user.locktime = now + timedelta(minutes=2)
        user.project_id = project.id
        user.env = Env.preprod
        await session.commit()
        return user
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The user is already busy",
    )


@router.patch("/{project_id}/user/{user_id}")
async def release_lock(
    project: Project = Depends(project_by_id),
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Снятие блокировки с пользователя и отвязывание от Проекта"""
    now = datetime.utcnow()
    if now < user.locktime:
        user.locktime = now
        user.project_id = None
        user.env = Env.stage
        await session.commit()
        return user
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The user already free",
    )


@router.get("/", response_model=list[Project])
async def get_projects(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Получение всех проектов"""
    return await crud.get_projects(session=session)


@router.post(
    "/",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    product_in: ProjectCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Создание Проекта"""
    return await crud.create_project(session=session, project_in=product_in)


@router.get("/{project_id}/", response_model=Project)
async def get_project(
    project: Project = Depends(project_by_id),
):
    """Получение Проекта по id"""
    return project


@router.delete("/{project_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project: Project = Depends(project_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    """Удаление Проекта"""
    await crud.delete_project(session=session, project=project)
