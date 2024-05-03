from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = MappedColumn(primary_key=True)
