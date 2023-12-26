from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# from app.db import get_session, init_db
from app.api import users
from app.api.users.endpoints import UserRouter

app = FastAPI()

app.include_router(UserRouter, prefix="/users", tags=["users"])

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
