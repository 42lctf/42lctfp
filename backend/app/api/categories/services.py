from uuid import uuid4

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from ..users.general_utils import get_user_by_token
from .schemas import CreateNewCategoryRequest
from .models import Category


def crete_new_category(body: CreateNewCategoryRequest, access_token: str, db: Session):
    user = get_user_by_token(access_token, db)
    if not user.is_user_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create category"
        )
    category_name = db.query(Category).filter(Category.name == body.name).first()
    if category_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists"
        )
    if category_name.display_order == body.display_order:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Display order already exists"
        )
    if len(body.name) > 50:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Name too long"
        )
    if body.display_order < 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Display order must be positive"
        )
    category = Category(
        id=uuid4(),
        display_order=body.display_order,
        name=body.name,
        created_at=body.created_at,
        updated_at=body.updated_at
    )
    db.add(category)
    db.commit()
    db.refresh(category)