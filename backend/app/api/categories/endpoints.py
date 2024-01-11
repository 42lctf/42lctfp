from typing import Annotated, Union

from fastapi import APIRouter, status, Cookie, Depends
from sqlalchemy.orm import Session

from .schemas import CreateNewCategoryRequest
from .services import crete_new_category
from app.db import get_session

CategoryRouter = APIRouter()


@CategoryRouter.get('/categories/new', status_code=status.HTTP_201_CREATED)
async def create_new_category(body: CreateNewCategoryRequest, access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    crete_new_category(body, access_token, db)
    return {"message": "New category created successfully"}
