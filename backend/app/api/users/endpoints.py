from fastapi import APIRouter

from .auth.endpoints import UserAuthRouter
from .me.endpoints import MeRouter
from .admin.endpoints import AdminRouter


UserRouter = APIRouter()

UserRouter.include_router(UserAuthRouter)
UserRouter.include_router(MeRouter)
UserRouter.include_router(AdminRouter)
