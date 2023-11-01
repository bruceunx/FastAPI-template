import sys
import os

import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext

parent_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir))

sys.path.append(parent_folder)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture(scope="module")
def client():
    os.environ["TEST_API"] = "Start"
    from main import app
    from db import DATABASE_URL, Base, engine
    if "test" not in DATABASE_URL:
        return
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker
    from models.users import User
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    with SessionLocal() as sess:
        sess.add(
            User(username="admin",
                 password=pwd_context.hash("admin123#"),
                 group=1))
        sess.add(
            User(username="test",
                 password=pwd_context.hash("test123"),
                 group=0))
        sess.commit()

    yield TestClient(app)
    del os.environ["TEST_API"]
