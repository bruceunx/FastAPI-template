from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime
)
from sqlalchemy.sql import func
from db import Base  # type: ignore


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), unique=True, index=True)
    password = Column(String(30), nullable=False)
    group = Column(Integer, default=0)

class Logger(Base):
    __tablename__ = "logger"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_stamp = Column(DateTime, server_default=func.now())
    host = Column(String(30), nullable=False)
    username = Column(String(30), nullable=False)
