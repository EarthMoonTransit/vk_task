from .base import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn


class Product(Base):
    __tablename__ = 'products'

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
