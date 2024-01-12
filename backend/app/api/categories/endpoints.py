from typing import Annotated, Union

from fastapi import APIRouter, status, Cookie, Depends
from sqlalchemy.orm import Session

from .schemas import CreateNewCategoryRequest, PatchCategory
from .services import create_new_category, get_categories, update_category, delete_category
from app.db import get_session

CategoryRouter = APIRouter()


@CategoryRouter.get('', status_code=status.HTTP_200_OK)
async def get_all_categories(access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    categories = get_categories(access_token, db)
    return {"categories": categories}

@CategoryRouter.post('', status_code=status.HTTP_201_CREATED)
async def create_new_category_request(body: CreateNewCategoryRequest, access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    create_new_category(body, access_token, db)

@CategoryRouter.patch('/{category_id}', status_code=status.HTTP_200_OK)
async def update_category_request(category_id: str, body: PatchCategory, access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    update_category(category_id, body, access_token, db)
    return {"message": "category successfully modified"}


@CategoryRouter.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_request(category_id: str, access_token: Annotated[Union[str, None], Cookie()] = None, db: Session = Depends(get_session)):
    delete_category(category_id, access_token, db)
    return {"message": "category successfully modified"}