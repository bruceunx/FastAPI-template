import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from databases import Database

# DATABASE_URL = "mysql+pymysql://root:123456@localhost/test"
# engine = create_engine(
#     DATABASE_URL,
#     pool_size=32,
#     pool_recycle=3600,
#     pool_pre_ping=True,
#     echo=False,
# )

if "TEST_API" in os.environ:
    # DATABASE_URL = "sqlite:///api.db"
    DATABASE_URL = "sqlite:///test.db"
else:
    DATABASE_URL = "sqlite:///api.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=False,
)

Base = declarative_base()

DB = Database(DATABASE_URL)
