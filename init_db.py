from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from db import engine, Base
from models import User
Base.metadata.drop_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base.metadata.create_all(engine)
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
