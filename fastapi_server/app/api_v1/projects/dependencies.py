import uuid
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Path, Depends, HTTPException, status

from app.db import db_helper
from app.core.models import Project
from . import crud


async def project_by_id(
    project_id: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Project:
    project = await crud.get_project(session=session, project_id=project_id)
    if project is not None:
        return project
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Project {project_id} not found"
    )
