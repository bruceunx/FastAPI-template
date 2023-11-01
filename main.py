from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers.v1 import users as v1_users_router  # type: ignore
from routers.v1 import products as v1_products_router  # type: ignore

from db import DB, Base, engine

Base.metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await DB.connect()


@app.on_event("shutdown")
async def shutdown():
    await DB.disconnect()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_users_router.router,
                   prefix="/v1/user",
                   tags=["Version 1"])
app.include_router(v1_products_router.router,
                   prefix="/v1/product",
                   tags=["Version 1"])
