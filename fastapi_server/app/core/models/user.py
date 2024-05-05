from typing import TYPE_CHECKING
from .base import Base
from enum import Enum
from app.core.helpers import Env, Domain
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy import String, DateTime, ForeignKey, LargeBinary
from datetime import datetime

if TYPE_CHECKING:
    from .project import Project


class User(Base):
    """Модель Пользователя"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
    login: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=True)
    project: Mapped["Project"] = relationship(back_populates="users")
    env: Mapped[Enum] = mapped_column(
        PgEnum(Env, name="env"), nullable=False, default=Env.stage
    )
    domain: Mapped[Enum] = mapped_column(
        PgEnum(Domain, name="domain"), nullable=False, default=Domain.slave
    )
    locktime: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
