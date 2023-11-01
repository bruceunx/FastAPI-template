from sqlalchemy import select, insert

from models.users import User, Logger  # type: ignore

from db import DB


async def get_user(username: str):
    query = select(User).where(User.username == username)
    return await DB.fetch_one(query=query)

async def create_logger(username:str, host:str):
    query = insert(Logger)
    await DB.execute(query, values={"username": username, "host":host})
