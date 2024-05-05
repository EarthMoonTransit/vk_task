import uuid
from typing import Annotated
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Path, Depends, HTTPException, status

from . import crud
from app.db import db_helper
from app.core.models import User


async def user_by_id(
    user_id: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    user = await crud.get_user(session=session, field=user_id)
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
    )
