import uuid
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Project
from .schemas import ProjectCreate


async def get_projects(session: AsyncSession) -> list[Project]:
    stmt = select(Project)
    result: Result = await session.execute(stmt)
    projects = result.scalars().all()
    return list(projects)


async def get_project(session: AsyncSession, project_id: uuid.UUID) -> Project | None:
    return await session.get(Project, project_id)


async def create_project(session: AsyncSession, project_in: ProjectCreate):
    project = Project(**project_in.model_dump())
    session.add(project)
    await session.commit()
    return project


async def delete_project(
    session: AsyncSession,
    project: Project,
) -> None:
    await session.delete(project)
    await session.commit()
