import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, declared_attr


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[uuid.UUID] = MappedColumn(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
