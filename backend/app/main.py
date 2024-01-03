from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.middleware.cors import CORSMiddleware

from app.api import users
from app.api.users.endpoints import UserRouter

app = FastAPI()

origin = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter, prefix="/api/v1/users", tags=["users"])


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
