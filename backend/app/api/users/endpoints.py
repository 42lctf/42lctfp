from fastapi import APIRouter, status
from .models import User
from .schema import UserRequest
from .services import create_user
from uuid import uuid4

UserRouter = APIRouter()

@UserRouter.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserRequest):
    new_user = User(id=uuid4(), nickname=user.nickname, description="default description")
    return await create_user(user)

# @UserRouter.get("/users", response_model=list[UserRequest])
# async def get_users():
#     return await get_users()