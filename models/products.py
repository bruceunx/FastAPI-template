from sqlalchemy import (
    Column,
    String,
    Integer,
)

from db import Base  # type: ignore


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
