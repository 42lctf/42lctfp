from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session, init_db
from app.models import Users

app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.get("/users", response_model=list[Users])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Users))
    songs = result.scalars().all()
    return [Users(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]
