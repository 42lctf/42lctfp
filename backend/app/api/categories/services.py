from uuid import uuid4
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import asc

from ..users.general_utils import get_user_by_token
from .schemas import CreateNewCategoryRequest, CategoryRequest, PatchCategory
from .models import Category
from app.api.challenges.models import Challenge


def get_categories(access_token: str, db: Session) -> List[Category]:
    user = get_user_by_token(access_token, db)
    if not user.is_user_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can retrieve categories"
        )
    categories = db.query(Category).order_by(asc(Category.display_order)).all()
    if not categories:
        return []
    filtered_categories = [
        CategoryRequest(name=category.name, display_order=category.display_order)
        for category in categories
    ]
    return filtered_categories

def create_new_category(body: CreateNewCategoryRequest, access_token: str, db: Session):
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
    if category_name and category_name.display_order == body.display_order:
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

def update_category(category_id: str, body: PatchCategory, access_token: str, db: Session):
    user = get_user_by_token(access_token, db)
    if not user.is_user_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update category"
        )
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="category not found"
        )
    category_name = db.query(Category).filter(Category.name == body.name, Category.id != category_id).first()
    if category_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="category name already exists"
        )
    if len(body.name) > 50:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="category name too long"
        )

    category.name = body.name
    category.display_order = body.display_order

    db.commit()
    db.refresh(category)

def delete_category(category_id: str, access_token: str, db: Session):
    user = get_user_by_token(access_token, db)
    if not user.is_user_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete category"
        )
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="category not found"
        )
    challenges_using_category = db.query(Challenge).filter(Challenge.category_id == category_id).all()
    if challenges_using_category:
        challenge_names = [challenge.title for challenge in challenges_using_category]
        challenges_str = ', '.join(challenge_names)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"category is used by challenges: {challenges_str}. Cannot delete."
        )

    db.delete(category)
    db.commit()