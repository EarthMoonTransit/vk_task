import uuid
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreate
from app.core.models import User
from app.core.helpers import Env, Domain
from app.auth.utils import hash_password


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, field: uuid.UUID | EmailStr) -> User | None:
    return await session.get(User, field)


async def create_user(session: AsyncSession, user_in: UserCreate):
    data = user_in.model_dump()
    data["password"] = hash_password(data["password"])
    user = User(**data)
    session.add(user)
    await session.commit()
    return user
