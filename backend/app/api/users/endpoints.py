from fastapi import APIRouter

from .auth.endpoints import UserAuthRouter
from .me.endpoints import MeRouter


UserRouter = APIRouter()

UserRouter.include_router(UserAuthRouter)
UserRouter.include_router(MeRouter)
