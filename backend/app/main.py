from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.users.endpoints import UserRouter
from app.api.categories.endpoints import CategoryRouter
from app.api.users.admin.endpoints import AdminRouter

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
app.include_router(CategoryRouter, prefix="/api/v1/categories", tags=["categories"])
app.include_router(AdminRouter, prefix="/api/v1/admin", tags=["admins"])


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
