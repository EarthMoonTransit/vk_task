from typing import TYPE_CHECKING

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from .user import User


class Project(Base):
    """Модель Проекта"""

    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(back_populates="project")
